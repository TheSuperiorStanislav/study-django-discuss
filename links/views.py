from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.views.generic import (
    View,
    CreateView,
    DetailView,
    TemplateView,    
)
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator

from links.models import Link, Comment
from links.forms import CommentModelForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        now = timezone.now()
        submissions = Link.objects.all()
        for submission in submissions:
            num_votes = submission.upvotes.count()
            num_commments = submission.comment_set.count()

            num_days = (now - submission.submitted_on).days
            submission.rank = num_votes + num_commments - num_days
        
        sorted_submissons = sorted(submissions, key = lambda x: x.rank, reverse = True)
        ctx['submissions'] = sorted_submissons
        return ctx


class NewSubmissionView(CreateView):
    model = Link
    fields = (
        'title',
        'url',
    )

    template_name = 'new_submission.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewSubmissionView,self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new_link = form.save(commit = False)
        new_link.submitted_by = self.request.user
        new_link.save()

        self.object = new_link 
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('submission-detail', kwargs={'pk': self.object.pk})

class SubmissionDetailView(DetailView):
    model = Link
    template_name = 'submission_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(SubmissionDetailView, self).get_context_data(**kwargs)

        submission_comments = Comment.objects.filter(commented_on = self.object, in_reply_to__isnull = True)
        ctx['comments'] = submission_comments

        ctx['comments_form'] = CommentModelForm(initial = { 'link_pk':self.object.pk })

        return ctx

class NewCommentView(CreateView):
    form_class = CommentModelForm
    http_method_names = (
        'post',
        )
    template_name = 'comment.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewCommentView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        parent_link = Link.objects.get(pk = form.cleaned_data['link_pk'])
        new_comment = form.save(commit = False)
        new_comment.commented_on = parent_link
        new_comment.commented_by = self.request.user
        new_comment.save()
 
        return HttpResponseRedirect(reverse('submission-detail', kwargs={'pk': parent_link.pk}))
    
    def get_initial(self):
        initial_data = super(NewCommentView,self).get_initial()
        initial_data['link_pk'] = self.request.GET['link_pk']

        return super().get_initial()

    def get_context_data(self, **kwargs):
        ctx = super(NewCommentView, self).get_context_data(**kwargs)
        ctx['submission'] = Link.objects.get(pk=self.request.GET['link_pk'])

        return ctx
class NewCommentReplyView(CreateView):
    form_class = CommentModelForm
    template_name = 'comment_reply.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NewCommentReplyView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(NewCommentReplyView, self).get_context_data(**kwargs)
        ctx['parent_comment_pk'] = Comment.objects.get(pk=self.request.GET['parent_comment_pk'])

        return ctx

    def form_valid(self, form):
        parent_link = Link.objects.get(pk = form.cleaned_data['link_pk'])
        parent_comment = Comment.objects.get(pk = form.cleaned_data['parent_comment_pk'])
        
        new_comment = form.save(commit = False)
        new_comment.commented_on = parent_link
        new_comment.commented_by = self.request.user
        new_comment.in_reply_to = parent_comment
        new_comment.save()
 
        return HttpResponseRedirect(reverse('submission-detail', kwargs={'pk': parent_link.pk}))
    
    def get_initial(self):
        initial_data = super(NewCommentReplyView, self).get_initial()
        link_pk = self.request.GET['link_pk']
        initial_data['link_pk'] = link_pk
        parent_comment_pk = self.request.GET['parent_comment_pk']
        initial_data['parent_comment_pk'] = parent_comment_pk

        return initial_data

class UpvoteSubmissionView(View):
    def get(self, request, pk, **kwargs):
        link = Link.objects.get(pk = pk)
        link.upvotes.add(request.user)

        return HttpResponseRedirect(reverse('home'))

class RemoveUpvoteSubmissionView(View):
    def get(self, request, pk, **kwargs):
        link = Link.objects.get(pk = pk)
        link.upvotes.remove(request.user)

        return HttpResponseRedirect(reverse('home'))
