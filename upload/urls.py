
from django.conf.urls import include, url
from django.contrib import admin
import index
import subprocess
from django.conf import settings
from django.conf.urls.static import static

subprocess.Popen(["python3", 'index/'+"controlAnalysis.py"])

urlpatterns = [
	url(r'^admin/', admin.site.urls),

	url(r'^index/', include('index.urls')),
	url(r'login/$', index.views.login, name='login'),
	url(r'^$', index.views.homePage, name='home'),
	url(r'logout/$', index.views.logout, name='logout'),
	url(r'^upload/$', index.views.upload, name='upload'),
	url(r'^form/$', index.views.form, name='form'),
	url(r'^index/remove/(?P<filename>.+)/$', index.views.removeFile, name='removeFile'),
	url(r'^startAnalysis/(?P<project>.*)/$', index.views.startAnalysis, name='startAnalysis'),
	url(r'^results/$', index.views.results, name = 'results'),
	url(r'^getFileData/(?P<query>.*)', index.views.getFileData, name='getFileData'),
	url(r'^getVarData/(?P<query>.*)', index.views.getVarData, name='getVarData'),
	url(r'^analysisInformation/$', index.views.analysisInformation, name = 'analysisInformation'),
	url(r'^getProjectInfo/$', index.views.getProjectInfo, name='getProjectInfo'),
	url(r'^download/$', index.views.download, name='download'),
	url(r'^getDownloadContent/(?P<query>.*)', index.views.getDownloadContent, name='getDownloadContent'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
