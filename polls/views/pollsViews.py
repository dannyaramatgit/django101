from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Question
from django.urls import reverse

from django.views import View,generic
from ..forms import QuestionForm, ChoiceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def stam(request):
    response= render(request=request, template_name="polls/stam.html")
    return response


# class Index(LoginRequiredMixin, generic.ListView):
#     template_name="polls/index.html"
#     context_object_name = "latest_question_list"

#     def get_queryset(self):
#         return Question.objects.order_by('-pub_date')
#         # [:5]



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    view_count = request.COOKIES['view_count']
    context = {"latest_question_list":latest_question_list, 'view_count':view_count}
    
    # request.session['view_count'] = view_count +1
    resp = render(request=request,template_name='polls/index.html',context=context )
    resp.set_cookie('view_count',view_count +1)
    return resp

class Detail(View):
    # model = Question
    # template_name = "polls/detail.html"
    # context_object_name = "question"
    # def get_queryset(self):
    #     return super().get_queryset()
    def get(self, request, question_id):
           
        un = request.session.pop('username', 'guest')
        session_username = request.session.get('username', 'no one')
        expiratin = request.session.get_expiry_age()
        expiratin = request.session.get_expiry_date()
        request.session.set_expiry(60)
        expiratin = request.session.get_expiry_age()
        # request.session.flush()

        question = get_object_or_404(Question,pk=question_id)
        return render(request=request, template_name='polls/detail.html', context={'question': question})


class NewQuestion(View):
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            # question_text = form.cleaned_data['question_text']
            # pub_date = form.cleaned_data['pub_date']
            # q = Question(question_text, pub_date)
            # q.save()
            # Question.objects.create(question_text=question_text, pub_date=pub_date)
            form.save()
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            message = "failed validation"
            return render(request=request, template_name='polls/question_form.html', context={'form':form, 'message':message})
    
    def get(self, request):
        form = QuestionForm()
        return render(request=request, template_name='polls/question_form.html', context={'form':form})
    

class NewChoice(View):
    def post(self, request):
        form = ChoiceForm(request.POST)
        if form.is_valid():
            # choice_text = form.cleaned_data['choice_text']
            # votes = form.cleaned_data['votes']
            # # question = form.cleaned_data['question']
            # new_question = Question(question_text="will it work?",pub_date=timezone.now())
            # new_question.save()
            # q = Question(question_text, pub_date)
            # q.save()
            # Choice.objects.create(choice_text=choice_text, votes=votes, question=new_question)
            form.save()
            return HttpResponseRedirect(reverse('polls:index'))
    def get(self, request):
        form = ChoiceForm()
        return render(request=request, template_name='polls/choice_form.html', context={'form':form})
    
class Vote(View):
    def post(self,request, question_id):
        question = get_object_or_404(Question,pk=question_id)
        choice = question.choice_set.get(pk= request.POST['choice'])
        choice.votes = choice.votes +1
        choice.save()
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    def get(self,request, question_id):
        return HttpResponse('this was a get request')

