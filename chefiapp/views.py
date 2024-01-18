from django.shortcuts import render
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.exceptions import ValidationError
from datetime import datetime, date
from .models import ROLE_CHOICES, DEPARTMENT_CHOICES, User, PreCreateUser, MonthlySchedule, DailySchedule
from .helpers import MONTHS_DICT
from .models import User
import calendar

def caixa_view(request):
    return render(request, 'chefiapp/caixa.html')

def error_page_view(request):
    return render(request, 'chefiapp/error_page_view.html')

def new_month_data(request, user):
    if request.method == "POST":

        user = get_object_or_404(User, pk=user)
        selected_month = request.POST.get('selected_month')
        selected_year = request.POST.get('selected_year')

        with transaction.atomic():
            monthy_schedule, created = MonthlySchedule.objects.get_or_create(
                    user=user,
                    month=selected_month,
                    year=selected_year,
                )
            if created:
               # Redirect to the 'schedule' URL pattern with the 'user' argument
                return HttpResponseRedirect(reverse('schedule', kwargs={'user': user.id}) + '?message=Month%20Schedule%20Object%20Created.')

        # Redirect to 'schedule' page if the object already existed
        return HttpResponseRedirect(reverse('schedule'))
    
    # For GET requests or if the form wasn't submitted, redirect to 'schedule' page
    return HttpResponseRedirect(reverse('schedule'))

def save_schedule_data(request):
    if request.method == 'POST':

        # Decode the JSON data from the request body
        data = json.loads(request.body)

        start_hour = data.get('start_hour')
        end_hour = data.get('end_hour')
        user_id = data.get('userId')
        dayoff = data.get('dayoff')

        if dayoff:
            start_hour = '00:00'
            end_hour = '00:00'


        date = datetime.strptime(data.get('date'), "%Y-%m-%d")
        month = dict(MONTHS_DICT)[calendar.month_name[date.month]]
        year = date.year

        monthly_schedule = MonthlySchedule.objects.get(user=user_id, month=month, year=year)
        
        try:
            with transaction.atomic():
                # Get or create the DailySchedule
                
                daily_schedule, created = DailySchedule.objects.get_or_create(
                    monthly_schedule=monthly_schedule,
                    date=date,
                    defaults={'start_hour': start_hour, 'end_hour': end_hour, 'is_dayoff':dayoff}
                )

                if not created:
                    # Update the existing DailySchedule object with new values
                    daily_schedule.start_hour = start_hour
                    daily_schedule.end_hour = end_hour
                    daily_schedule.is_dayoff = dayoff

                    daily_schedule.save()

                return JsonResponse({
                    'start_hour': start_hour,
                    'end_hour': end_hour,
                    'dayoff': dayoff
                    })
            
        except DailySchedule.DoesNotExist:
            # Handle case when DailySchedule doesn't exist for given conditions
            return JsonResponse({'error': 'DailySchedule not found'}, status=404)
        except Exception as e:
            # Handle other error scenarios
            return JsonResponse({'error': str(e)}, status=500)

def get_schedule_data(request):
    if request.method == 'GET':
        user_id = request.GET.get('userId')
        date = request.GET.get('date')

        # Fetch data based on user_id and date
        try:
            daily_schedule = DailySchedule.objects.get(
                monthly_schedule__user_id=user_id,
                date=date
            )

            # Return the data as JSON with success status
            return JsonResponse({
                'status': 'success',
                'start_hour': daily_schedule.start_hour,
                'end_hour': daily_schedule.end_hour,
                'dayoff': daily_schedule.is_dayoff,
            })
        except DailySchedule.DoesNotExist:
            return JsonResponse({'status': 'failure', 'message': 'No object found for the given settings'}, status=200)
    
    
def update_schedule_data(request):
    if request.method == 'POST':

            data = json.loads(request.body)
            user_id = data.get('user_id')
            date_str = data.get('date')
            start_hour = data.get('start_hour')
            end_hour = data.get('end_hour')

            print(f"data: {data}")

            # Convert date string from "DD/MM/YYYY" to "YYYY-MM-DD" format
            parsed_date = datetime.strptime(date_str, '%d/%m/%Y').date()

            # Extract month and year from parsed_date
            month = parsed_date.strftime('%B')  # Get month name as a string
            year = parsed_date.year
            print(f"month: {month}")
            print(f"year: {year}")

            return JsonResponse({'success': 'Data asked successfully'})



    return JsonResponse({'error': 'Invalid request'}, status=400)

def schedule_view(request, user):
    
    current_user = request.user
    try:
        schedule_user = get_object_or_404(User, pk=user)

        today = date.today().isoformat()
    
        # Filter MonthlySchedule objects for the current user
        user_calendar = MonthlySchedule.objects.filter(user=schedule_user)

        user_days = DailySchedule.objects.filter(monthly_schedule__in=user_calendar).order_by('date')

        # Defining the range of years
        current_year = datetime.now().year
        start_year = 2022
        years = years = [(year, str(year)) for year in range(start_year, current_year + 1)]
        # Get the current month as a number
        current_month_number = datetime.now().month

        # Get the name of the current month based on the number
        current_month_name = calendar.month_name[current_month_number]


        return render(request, 'chefiapp/schedule.html', {
            'months':MONTHS_DICT,
            'years':years,
            'current_month': current_month_name,
            'current_year': current_year,
            'schedule_user':schedule_user,
            'user_calendar':user_calendar,
            'user_days':user_days,
            'user':current_user,
            'today':today
        })
    
    except User.DoesNotExist:
        # Redirect to a custom error page or show a specific error message
        return HttpResponseRedirect(reverse('schedule'), {
            'user':current_user,
        })

# PRE-CREATE NEW STAFF MEMBERS
def new_staff(request):

    # Manager ID that is creating the new instance
    user = request.user

    allUsers = User.objects.all()

    if request.user.is_authenticated:
        if request.method == "POST":
            if user.role in ['management', 'admin']:

                name = request.POST["name"]
                email = request.POST["email"]
                department = request.POST["department"]

                new_user = PreCreateUser(name=name, email=email, department=department)
                new_user.save()

                return render(request, 'chefiapp/new_profile.html', {
                    'user':user,
                    'message': "User pre-created successfully",
                    'new_user': new_user,
                })

            else:
                return render(request, 'chefiapp/new_staff.html', {
                    "message":"You are trying to change data you don't have permissions!"
                })

        else:
             # Access user information
            user = request.user

            # Retrieve all users
            allUsers = User.objects.all()

            return render(request, 'chefiapp/new_staff.html', {
                'user': user,
                'allUsers': allUsers,
                'role_choices': ROLE_CHOICES,
                'department_choices': DEPARTMENT_CHOICES,
            })
    else:
        HttpResponseRedirect(reverse('login'))

# Create your views here.
def index(request):
    return render(request, "chefiapp/index.html")

# Login View
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)


        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'chefiapp/login.html', {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, 'chefiapp/login.html')

# Register View
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chefiapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chefiapp/register.html", {
                "message": "Username already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'chefiapp/register.html')

# Logout View
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

# Profile with personal information of the user.
@login_required
def profile_view(request, id):
    
    # Check for authenticated user
    if request.user.is_authenticated:
        user = User.objects.get(pk=id)
        role_choices = ROLE_CHOICES
        department_choices = DEPARTMENT_CHOICES
        actualUser = request.user
        newDateJoined = None
        newDateOfBirth = None
        today = date.today()

        # Serialize actualUser object
        actualUser_json = json.dumps({
            'id': actualUser.id,
            'username': actualUser.username,
            'role': actualUser.role,  # Replace this with your actual attribute names
            'department': actualUser.department,  # Replace this with your actual attribute names
        })

        if request.method == "POST":
       
            if actualUser.role in ['management', 'admin'] or actualUser == User.objects.get(pk=id):
                
                form_data = request.POST
           
                # Prompt to get the input form for each feature
                email = form_data.get("email")
                name = form_data.get("name")
                address = form_data.get("address")
                department = form_data.get("department")
                form_date_of_birth = form_data.get("date_of_birth")
                dateJoined = form_data.get("dateJoined")


                try:
                    # Attempt to parse the date_of_birth
                    if form_date_of_birth:
                        newDateOfBirth = datetime.strptime(form_date_of_birth, '%Y-%m-%d').date()

                    if dateJoined:
                        newDateJoined = datetime.strptime(dateJoined, '%Y-%m-%d').date()
                    
                    if newDateJoined or newDateOfBirth:

                        # Calculate age based on the difference between hiring date and date of birth
                        age_at_hiring = newDateJoined.year - newDateOfBirth.year - ((newDateJoined.month, newDateJoined.day) < (newDateOfBirth.month, newDateOfBirth.day))

                        # Adjust age if the hiring month and day are before the birth month and day
                        if (newDateJoined.month, newDateJoined.day) < (newDateOfBirth.month, newDateOfBirth.day):
                            age_at_hiring -= 1  # Subtract 1 if the hiring date is before the birth date in the same year
                            print(age_at_hiring)

                        if newDateJoined > today:   
                            error_message = "Invalid date: The joined date cannot be in the future."
                            return render(request, 'chefiapp/profile.html', 
                                {'form_user': user,
                                'role_choices': role_choices,
                                'department_choices': department_choices,
                                'actualUser': actualUser_json,
                                'message_type': "error",
                                "message": error_message
                            })
                        
                        # Check if the age is less than 16
                        if age_at_hiring < 16:
                            error_message = "Invalid age. We don't hire kids :)"
                            return render(request, 'chefiapp/profile.html', 
                                {'form_user': user,
                                'role_choices': role_choices,
                                'department_choices': department_choices,
                                'actualUser': actualUser_json,
                                'message_type': "error",
                                "message": error_message
                            })
                    

                except ValueError as e:
                    # Handle the case where the date format is incorrect
                    error_message = f"Error: {e}. Please provide the date in the format YYYY-MM-DD."
                    return render(request, 'chefiapp/profile.html', {
                        'form_user': user, 'role_choices': role_choices,
                        'department_choices': department_choices,
                        'actualUser': actualUser_json,
                        'message_type': "error",
                        "message": error_message})

                # Check for changes and update the user object accordingly
                changes = {}

                if newDateJoined != user.date_joined and newDateJoined is not None:
                    changes['date_joined'] = newDateJoined

                if newDateOfBirth != user.date_of_birth and newDateOfBirth is not None:
                    changes['date_of_birth'] = newDateOfBirth
                        
                if user.email != email and email is not None:
                    changes['email'] = email

                if user.name != name and name is not None:
                    changes['name'] = name

                if user.address != address and address is not None:
                    changes['address'] = address

                if user.department != department and department is not None:
                    changes['department'] = department


                if not changes:  # If no changes detected
                    return render(request, 'chefiapp/profile.html', 
                        {'form_user': user,
                        'role_choices': role_choices,
                        'department_choices': department_choices,
                        'actualUser': actualUser_json,
                        'message_type': "info",
                        "message": "No changes detected"
                    })

                try:
                    # Update only the changed fields
                    User.objects.filter(pk=id).update(**changes)
                    user.refresh_from_db()  # Refresh the user object after update

                    return render(request, 'chefiapp/profile.html', {
                        'actualUser':actualUser_json,
                        'form_user':user,
                        'role_choices': role_choices,
                        'department_choices': department_choices,
                        'message_type': "success",
                        "message":"User changed successfully"
                    })
                
                # Add your code for redirection or success message rendering
                except ValidationError as e:
                    # Handle ValidationError
                    error_message = str(e)
                    return render(request, 'chefiapp/profile.html', {
                        'form_user': user,
                        'role_choices': role_choices,
                        'department_choices': department_choices,
                        'actualUser':actualUser_json,
                        "message": error_message  # Pass the error message to the template
                    })
            else:
                return render(request, 'chefiapp/profile.html', {
                    "message":"You are trying to change data you don't have permissions!"
                })
        else: 
            
            return render(request, 'chefiapp/profile.html', {
                'form_user':user,
                'role_choices': role_choices,
                'department_choices': department_choices,
                'actualUser':actualUser_json,
            })  
    else:
        HttpResponseRedirect(reverse('login'))

# Staff View (different for every role of staff)
def staff_view(request):

    if request.user.is_authenticated:
        # Access user information
        user = request.user

        # Retrieve all users
        allUsers = User.objects.all()
        new_staff = PreCreateUser.objects.all()

        return render(request, 'chefiapp/staff.html', {
            'user': user,
            'allUsers': allUsers,
            'new_staff': new_staff,
        })
    else:
        HttpResponseRedirect(reverse('login'))
    