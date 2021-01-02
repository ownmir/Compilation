from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Category, Topic, Post
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import NewTopicForm, PostForm
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django_otp.decorators import otp_required
from two_factor.views.mixins import OTPRequiredMixin


# Create your views here.
def simply_first(request):
    categories = Category.objects.all()
    return render(request, 'simple_forum/first.html', {'categories': categories})


def category_topics(request, pk):
    category = get_object_or_404(Category, pk=pk)
    queryset = category.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    for t in queryset:
        print('t.replies (', t.subject,') -', t.replies)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 20)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        # перехід до першої сторінки
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # ймовірно, користувач намагався додати номер сторінки
        # in the url, so we fallback to the last page
        # в URL-адресу, тому ми переходимо на останню сторінку
        topics = paginator.page(paginator.num_pages)
    return render(request, 'simple_forum/topics.html', {'category': category, 'topics': topics})


@login_required
@otp_required
def new_topic(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # user = User.objects.first()  # DONE: get the currently logged in user
    if request.method == 'POST':
        print('Post')
        form = NewTopicForm(request.POST)
        if form.is_valid():
            print('valid')
            topic = form.save(commit=False)
            topic.category = category
            topic.starter = request.user
            topic.subject = form.cleaned_data.get('subject')
            topic.save()
            print(topic)
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user,
                updated_by=request.user
            )
            print(post)
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        print('get')
        form = NewTopicForm()

    return render(request, 'simple_forum/new_topic.html', {'category': category, 'form': form})


# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'simple_forum/topic_posts.html', {'topic': topic})
#
#
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'simple_forum/topic_posts.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # Ми не хочемо, щоб один і той же користувач
        # оновлював сторінку, де підраховується кількість переглядів
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, category__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@login_required
@otp_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, category__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.updated_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'simple_forum/reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
# @method_decorator(otp_required, name='dispatch')
class PostUpdateView(OTPRequiredMixin, UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'simple_forum/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'  # not object

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.category.pk, topic_pk=post.topic.pk)
