from django.shortcuts import render
from django.db import connection
from .queries import (
    ANALYSIS_Q1, ANALYSIS_Q2, ANALYSIS_Q3,
    GET_LOCATIONS, GET_PARTICIPANTS, GET_MEETINGS, GET_METHODS, GET_OBSERVERS,
    FIND_PARTICIPANTS_BY_LOCATION,
    PARTICIPANT_STATS,
    ADD_OBSERVATION_INSERT,
    CHECK_PARTICIPANT_IN_MEETING,
    CHECK_OBSERVATION_EXISTS,
    GET_OBSERVER_AVG_CONFIDENCE
)


def dictfetchall(cursor):
    """Return all rows from a cursor as a list of dictionaries."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
# Create your views here.
def home(request):
    return render(request, 'Meetings_App/home.html')

def analysis(request):
    """Render the analytics dashboard with results from three SQL queries."""

    with connection.cursor() as cursor:
        cursor.execute(ANALYSIS_Q1)
        q1_rows = dictfetchall(cursor)

        cursor.execute(ANALYSIS_Q2)
        q2_rows = dictfetchall(cursor)

        cursor.execute(ANALYSIS_Q3)
        q3_rows = dictfetchall(cursor)

    context = {
        "q1_rows": q1_rows,
        "q2_rows": q2_rows,
        "q3_rows": q3_rows,
    }

    return render(request, 'Meetings_App/analysis.html', context)

def add_observation(request):
    """Validate form input and insert a new observation record."""
    error = None
    success = None
    warning = None


    with connection.cursor() as cursor:
        cursor.execute(GET_MEETINGS)
        meetings = [row[0] for row in cursor.fetchall()]

        cursor.execute(GET_PARTICIPANTS)
        participants = [row[0] for row in cursor.fetchall()]

        cursor.execute(GET_OBSERVERS)
        observers = [row[0] for row in cursor.fetchall()]

        cursor.execute(GET_METHODS)
        methods = [row[0] for row in cursor.fetchall()]

    if request.method == "POST":
        try:
            meeting_id = int(request.POST.get("mid"))
            participant_id = int(request.POST.get("pid"))
            observer_id = int(request.POST.get("oid"))
            method = request.POST.get("method", "").strip()
            cLevel = int(request.POST.get("cLevel"))

            if observer_id <= 0:
                raise ValueError("Observer ID must be a positive integer.")

            if not (1 <= cLevel <= 100):
                raise ValueError("Confidence level must be between 1 and 100.")
            if len(method) == 0:
                raise ValueError("Method is required.")

        except (TypeError, ValueError) as e:
            error = f"Invalid input: {e}"
        else:
            with connection.cursor() as cursor:

                cursor.execute(CHECK_PARTICIPANT_IN_MEETING, [meeting_id, participant_id])
                if cursor.fetchone() is None:
                    error = "Participant did not participate in the selected meeting."


                if not error:
                    cursor.execute(CHECK_OBSERVATION_EXISTS, [meeting_id, participant_id, observer_id])
                    if cursor.fetchone() is not None:
                        error = "An observation for this meeting, participant and observer already exists."


                if not error:
                    cursor.execute(ADD_OBSERVATION_INSERT, [meeting_id, observer_id, participant_id, method, cLevel])

                    success = "Observation added successfully!"


                    cursor.execute(GET_OBSERVER_AVG_CONFIDENCE , [observer_id])
                    avg_level = cursor.fetchone()[0]


                    if avg_level is not None and cLevel < avg_level:
                        warning = (
                            f"Warning: confidence level ({cLevel}) is significantly lower "
                            f"than the observer's average ({avg_level:.1f})."
                        )

    return render(
        request,
        "Meetings_App/add_observation.html",
        {
            "error": error,
            "success": success,
            "warning": warning,
            "meetings": meetings,
            "participants": participants,
            "observers": observers,
            "methods": methods,
        },
    )


def get_participants_base_context():
    with connection.cursor() as cursor:
        cursor.execute(GET_LOCATIONS)
        locations = [row[0] for row in cursor.fetchall()]

        cursor.execute(GET_PARTICIPANTS)
        participants = [row[0] for row in cursor.fetchall()]

    return {
        "locations": locations,
        "participants": participants,

        # Find participant
        "selected_location": "",
        "find_rows": [],
        "find_message": "",

        # Participant analytics
        "participant_id": "",
        "analyze_error": "",
        "observer_count": None,
        "meetings_without_observation": None,
        "top_observation_method": None,
    }


def handle_find_participant(request, context):
    location = request.POST.get("location", "").strip()
    context["selected_location"] = location

    if not location:
        context["find_message"] = "Please select a location."
        return

    with connection.cursor() as cursor:
        cursor.execute(FIND_PARTICIPANTS_BY_LOCATION, [location])
        rows = cursor.fetchall()

    context["find_rows"] = [row[0] for row in rows]

    if not context["find_rows"]:
        context["find_message"] = "No participants match the search conditions."


def handle_analyze_participant(request, context):
    participant_id_raw = request.POST.get("pid", "").strip()
    context["participant_id"] = participant_id_raw

    try:
        participant_id = int(participant_id_raw)
        if participant_id <= 0:
            raise ValueError()
    except (TypeError, ValueError):
        context["analyze_error"] = "Selected participant is invalid."
        return

    with connection.cursor() as cursor:
        cursor.execute(PARTICIPANT_STATS, [participant_id, participant_id, participant_id])
        row = cursor.fetchone()

    if row is None:
        context["analyze_error"] = "Unable to analyze the selected participant."
        return

    context["observer_count"] = row[0]
    context["meetings_without_observation"] = row[1]
    context["top_observation_method"] = row[2]


def participants(request):
    """Support participant search by location and participant-level summary analysis."""
    context = get_participants_base_context()

    if request.method == "POST":
        form_type = request.POST.get("form_type", "")

        if form_type == "find":
            handle_find_participant(request, context)

        elif form_type == "analyze":
            handle_analyze_participant(request, context)

    return render(request, "Meetings_App/participants.html", context)