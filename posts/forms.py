from django import forms
from tinymce import TinyMCE
from .models import Post, Comment
from django import forms
from PIL import Image


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = (
            'title', 'overview', 'content', 'thumbnail', 'categories', 'featured', 'previous_post', 'next_post')


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ('content', )


# ------------------Star Cross Gallery ---------------------------------
class ImageFileInput(forms.ClearableFileInput):

    def validate(self, value):
        return super.validate(value)


class ImageCreateForm(forms.Form):
    data = forms.FileField(widget=ImageFileInput(attrs={'multiple': True}))

    def clean(self):
        """ Validate files by checking they can be opened by PIL """
        # cleaned_data = super(ImageCreateForm, self).clean()
        image_files = self.files.getlist('data')
        invalid_images = []
        for img in image_files:
            try:
                i = Image.open(img)
                i.verify()
                i.close()
            except (IOError, SyntaxError):
                invalid_images += [img]
        if invalid_images:
            image_names = [i._name for i in invalid_images]
            raise forms.ValidationError("Unable to add invalid images: {0}".format(image_names))
