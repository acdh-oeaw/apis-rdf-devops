import json
import requests
import subprocess
from copy import deepcopy
from importlib import import_module
import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView

from . forms import form_user_login
from . utils import PROJECT_METADATA as PM
from . utils import PROJECT_TITLE_IMG, PROJECT_LOGO


def get_imprint_url():
    try:
        base_url = settings.ACDH_IMPRINT_URL
    except AttributeError:
        base_url = "https://redmine-service-issue.acdh.oeaw.ac.at/"
    try:
        redmine_id = settings.REDMINE_ID
    except AttributeError:
        redmine_id = "go-register-a-redmine-service-issue"
    return "{}{}".format(base_url, redmine_id)


class ImprintView(TemplateView):
    template_name = 'webpage/imprint.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imprint_url = get_imprint_url()
        r = requests.get(get_imprint_url())

        if r.status_code == 200:
            context['imprint_body'] = "{}".format(r.text)
        else:
            context['imprint_body'] = """
            On of our services is currently not available. Please try it later or write an email to
            acdh@oeaw.ac.at; if you are service provide, make sure that you provided ACDH_IMPRINT_URL and REDMINE_ID
            """
        return context


class GenericWebpageView(TemplateView):
    template_name = "webpage/index.html"

    def get_context_data(self, **kwargs):
        context = super(GenericWebpageView, self).get_context_data(**kwargs)
        context["apps"] = settings.INSTALLED_APPS
        return context

    def get_template_names(self):
        template_name = "webpage/{}.html".format(self.kwargs.get("template", "index"))
        try:
            loader.select_template([template_name])
            template_name = "webpage/{}.html".format(
                self.kwargs.get("template", "index")
            )
        except:
            template_name = "webpage/index.html"
        return [template_name]


#################################################################
#               views for login/logout                          #
#################################################################


def user_login(request):
    if request.method == "POST":
        form = form_user_login(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(request.GET.get("next", "/"))
            return HttpResponse("user does not exist")
    else:
        form = form_user_login()
        return render(request, "webpage/user_login.html", {"form": form})


def user_logout(request):
    logout(request)
    return render(request, "webpage/user_logout.html")


def handler404(request, exception):
    return render(request, "webpage/404-error.html", locals())


@login_required
def set_user_settings(request):
    res = dict()
    edit_views = request.GET.get("edit_views", False)
    if edit_views == "true":
        edit_views = True
    else:
        edit_views = False
    request.session["edit_views"] = edit_views
    res["edit_views"] = edit_views
    return HttpResponse(json.dumps(res), content_type="application/json")


def project_info(request):

    """
    returns a dict providing metadata about the current project
    """

    info_dict = deepcopy(PM)

    if request.user.is_authenticated:
        pass
    else:
        del info_dict["matomo_id"]
        del info_dict["matomo_url"]
    info_dict["title_img"] = PROJECT_TITLE_IMG
    info_dict["project_logo"] = PROJECT_LOGO
    info_dict["base_tech"] = "django"
    info_dict["framework"] = "apis"
    info_dict["version webpage"] = "{}/commit/{}".format(
        info_dict["github"],
        subprocess.check_output(
            ["git", "describe", "--always"], cwd=settings.BASE_DIR
        ).strip().decode("utf8"),
    )
    rest_settings = settings.REST_FRAMEWORK.get("DEFAULT_PERMISSION_CLASSES", [])
    if "ReadOnly" in " ".join(rest_settings):
        info_dict["public"] = "public"
    else:
        info_dict["public"] = "restricted"
    vers = []
    for v in info_dict['version']:
        res2 = dict()
        mod = import_module(v)
        res2['library'] = v
        res2["version"] = getattr(mod, '__version__', 'undefined')
        try:
            g_url = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], cwd="{}/{}/".format(settings.BASE_DIR, v)
            ).strip().decode('utf8')
            git_url_t = re.match('^\w+@(.+):(.+)\.git$', g_url)
            if git_url_t:
                g_url = "https://{}/{}".format(git_url_t.group(1), git_url_t.group(2))
            g_commit = subprocess.check_output(
                ["git", "describe", "--always"], cwd="{}/{}/".format(settings.BASE_DIR, v)
            ).strip().decode("utf8"),
            if not isinstance(g_commit, str):
                g_commit = g_commit[0]
            res2["git"] = "{}/commit/{}".format(g_url, g_commit)
        except Exception as e:
            print(e)
        vers.append(res2)
    info_dict['version'] = vers
    return JsonResponse(info_dict)
