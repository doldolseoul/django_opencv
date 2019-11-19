from django.shortcuts import render
from django.shortcuts import redirect
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage

def first_view(request):
    return render(request, 'opencv_webapp/first_view.html', {})


def upload_image(request):
    if request.method == 'POST': #사용자가 업로드 버튼 누르면 아래 부분 실행
        form = UploadImageForm(request.POST, request.FILES) #forms.py에 정의
        if form.is_valid(): # UploadImageForm input값들이 조건을 만족할 떄
            myfile = request.FILES['image']
            fs = FileSystemStorage() #장고 내장함수 FileSystemStorage 사용
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename) # 실제 파일 저장된 경로
	# image_size=fs.size(filename)
            context = {'form': form, 'uploaded_file_url': uploaded_file_url} #upload_image.html의 form태그와 이어준다
            return render(request, 'opencv_webapp/upload_image.html', context)

    else: # request.method == 'GET' / get요청(데이터불러오기)일 때 아래부분 실행
        form = UploadImageForm()
        context = {'form': form} # views.py에서 불러온 데이터를  dict에 넣고 render함수 통해서 html를 통해 사용자에게 보여준다
        return render(request, 'opencv_webapp/upload_image.html', context)

from .forms import ImageUploadForm
from django.conf import settings


from .cv_functions import cv_detect_face
def detect_face(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # DB에 실제로 저장하기 전에 추가로 Form(post)에 다른 데이터 추가 가능
            post.save() # DB에 실제로 Form에 모아진 데이터를 저장

            imageURL = settings.MEDIA_URL + form.instance.document.name
            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL) # 추후 구현 예정

            return render(request, 'opencv_webapp/detect_face.html', {'form':form, 'post':post})
            # post는 save() 후 DB에 저장된 ImageUploadModel 클래스 객체 자체를 갖고 있게 됨 (값이 있음 == True)
    else:
         form = ImageUploadForm()
    return render(request, 'opencv_webapp/detect_face.html', {'form':form})
