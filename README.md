Distinctiveness and Complexity: 
The reason I developed this web application was the need to keep a track on employee's schedule for a restaurant that I'm currently the manager. So, this project is unique because it's based in my own experience and my problem to be solved, all data and information needed to make this works comes from my daily life in the restarant.

The app satisfies the complexity required because it utilize Django (with 3 different models) and Javascript (including updating the database using fetch calls). The complexity of the project is not determined just by the number of different models created but buy the user-friendly experience that the apps delivers, all buttons, styles, borders, cards where created and designed properly to be useful, responsive and also with good appearance.

Inside the chefiapp's File we have all HTML templates.

Layout.html: Stores all the basic informations for the header and footer, it's used in all the other templates.

Index.html: The 'home' page, where the user is redirected after logging-in and also the main page of the web app.

login.html: The login page that allows the user to login or redirect to be registered.

register.html: The register pages allow the user to create an account and use the account inside the web app.

profile.html : Allows the user to see basic personal information and also to change the ones he thinks it has to be changed. Ones profiles can be seen by any other user, just by calling the id of the user in the url.
staff.html: Here there are created cards in a loop for all users with ther names, their job description and also a link to their schedule. All users can see the staff members and also see their profile or their schedule. But just the users with 'manager' status can change the profile data or change the schedule data.

Schedule.html : The most complex view page, where creates within a loop cards that represents the days of the month for a selected month and year. For the selected month the algorithm will create cards for all days and inside everyday if there is an object created for that exact day and user it will return the data stored in the database. If there's no data for a certain day, it'll let the card empty, but also editable.
When the user (with status manager) clicks on 'edit' button, it opens a form with a 'dayoff' switch and also start and end hours inputs. If the day-off input is set to True, the inputs will disappear and the user can save the day as a dayoff, this changes the day background color to gray. But, if the user switch the day-off switch to False, the input appears and the user can edit the start and end hour for that day, when the user is done editing, he can click in save and it creates a fetch call that checks with the backend the existence of an object for that exact date and user. If there is an object, it updates the object with the new input datas and returns sucessful. If not, it creates a new object for this day and user and store the input datas in the database.