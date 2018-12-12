from django.shortcuts import render


# Create your views here.
def translate_tutor(request):
    trunk_open_form_post = '<form method="post" novalidate>'
    trunk_csrf_token = '    {% csrf_token %}'
    trunk_input = '    <input type="hidden" name="next" value="{{ next }}">'
    trunk_include = '    {% include "includes/form.html" %}'
    trunk_button = '    <button type="submit" class="btn btn-primary btn-block">Log in</button>'
    trunk_close_form = '</form>'
    # for_em = ''
    return render(request, 'translate_tutor/trans_tutor.html', {'trunk_open_form_post': trunk_open_form_post,
        'trunk_csrf_token': trunk_csrf_token, 'trunk_input': trunk_input, 'trunk_include': trunk_include,
        'trunk_button': trunk_button, 'trunk_close_form': trunk_close_form})


def translate_tutor6(request):
    return render(request, 'translate_tutor/trans_tutor6.html')


def translate_tutor7(request):
    return render(request, 'translate_tutor/trans_tutor7.html')