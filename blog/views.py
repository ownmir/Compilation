from django.shortcuts import render, get_object_or_404

from wagtail.core.models import Page
from wagtail.search.models import Query


def search(request):
    # Search
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = Page.objects.live().search(search_query)

        # Запишите запрос, чтобы Wagtail мог предложить продвигаемые результаты
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Render template
    render(request, 'blog/search_results.html', {'search_query': search_query, 'search_result': search_results})


def indent(request):
    ieven = request.GET.get('indentEven', 1)
    iodd = request.GET.get('indentOdd', 10)
    trunk_code = '{{ var|filter_function:"argument" }}'
    if ieven and iodd:
        print('ieven ()', ieven, 'iodd (ieven and iodd - true)', iodd)
        return render(request, 'blog/indent_x.html', {'ieven': ieven, 'iodd': iodd, 'trunk_code': trunk_code})
    else:
        from .models import IndentX
        indent_object = get_object_or_404(IndentX, pk=12)
        ieven, iodd = indent_object.how_many_even, indent_object.how_many_odd
        print('iodd', iodd)
        return render(request, 'blog/indent_x.html', {'ieven': 1, 'iodd': 10, 'trunk_code': trunk_code})