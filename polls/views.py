from django.views.generic import TemplateView, DetailView
from django_listing import *
import django_listing

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
    # return HttpResponse("You're voting on question %s." % question_id)

# ################################################################################################################ #
class SimpleListing(Listing):
    # If no columns are specified, django_listing will auto-detect them
    # based on data provided (list of dicts, list of lists, model, query set etc...
    per_page = 10
    
class ToolbarSimpleListing(SimpleListing):
    per_page = 8

class ToolbarEmployeeDivListing(DivListing):
    # override sorting choices (with tuples syntax)
    toolbar_sortselect__choices=(('first_name','First name A-Z'),
                                 ('-first_name','First name Z-A'),
                                 ('age','Youngest first'),
                                 ('-age','Oldest first'))
    attrs = {'class':'div-striped div-hover div-bordered'}
    per_page = 8

class EmployeeThumbnailsListing(DivListing):
    div_template_name = 'demo/thumbnails.html'
    attrs = {'class':''}
    # will add the 'thumbnail' class to the container
    # means that one have to set 'div.row-container.thumbnail'
    # in .css to modify the look
    theme_div_row_container_class = 'thumbnail'
    per_page = 16

class ToolbarEmployeeThumbnailsListing(EmployeeThumbnailsListing):
    per_page = 16
    # override sorting choices (with one big string syntax)
    toolbar_sortselect__choices=('first_name:First name A-Z,'
                                 '-first_name:First name Z-A,'
                                 'age:Youngest first,'
                                 '-age:Oldest first')

class ToolbarEmployeeBigThumbnailsListing(ToolbarEmployeeThumbnailsListing):
    div_template_name = 'demo/big_thumbnails.html'
    per_page = 9
    toolbar_perpageselect__choices = '9,18,27,-1:All' #overrides ToolbarListing.toolbar PerPageSelectToolbarItem choices attribute
    theme_div_row_container_class = 'big-thumbnail'


class ToolbarListing(ListingVariations):
    variations_classes = (
        ToolbarSimpleListing,
        ToolbarEmployeeDivListing,
        ToolbarEmployeeThumbnailsListing,
        ToolbarEmployeeBigThumbnailsListing,
    )
    toolbar = Toolbar(
        ExportSelectToolbarItem(),
        SortSelectToolbarItem(),
        VariationsToolbarItem(
            labels=('Listing', 'Detailed', 'Thumbnails', 'Big thumbnails'),
            icons=('listing-icon-menu-2', 'listing-icon-th-list-4',
                   'listing-icon-th-3', 'listing-icon-th-large-2')),
        PerPageSelectToolbarItem(choices='8,16,32,64,-1:All'),
    )
    toolbar_placement = 'both'
    per_page = 8
    paginator_has_first_last = True
    exclude_columns = 'interests'


class ToolbarListingView(ListingView):
    template_name = 'polls/toolbar.html'
    context_classes = (ToolbarListing,
                       ToolbarSimpleListing,
                       Choice,
                       )


class BasicUsageListingView(TemplateView):
    template_name = 'polls/toolbar.html'
    extra_context = dict(employees_as_model=Choice)

