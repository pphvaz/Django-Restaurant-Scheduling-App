<h2>Django Web Application for Restaurant Employee Scheduling</h2>
<h2>Overview</h2>
This web application was developed to address the need for efficient employee schedule management in a restaurant setting. As the manager of a restaurant, I faced challenges in keeping track of the schedules, and this project stems from a desire to create a solution based on my firsthand experience and daily operational needs.

<h2>Usage</h2>
<h5>Profile Editing:</h5>
Users can view and edit their profiles, with managers having the additional ability to edit staff profiles.

<h5>Staff Viewing:</h5>
All users can view staff details and navigate to individual profiles and schedules.

<h5>Schedule Management:</h5>
Managers can edit schedules, setting day-offs or modifying working hours for each staff member on specific days.

<h2>Project Structure</h2>
Files in chefiapp
<b>Layout.html:</b> Centralizes basic information for the header and footer, utilized across all other templates.

 Serves as the 'home' page, welcoming users after logging in and acting as the main gateway to the application.

<b>login.html:</b> Allows users to log in or navigate to the registration page.

<b>register.html</b>: Enables users to create an account for accessing the web application.

<b>profile.html:</b> Provides users with access to basic personal information and the ability to make necessary updates. User profiles can be viewed by others simply by using the user's ID in the URL.

<b>staff.html:</b> Displays cards for all users, showcasing their names, job descriptions, and links to their schedules. All users can view staff details and schedules, but only users with 'manager' status can edit profile and schedule data.

<b>schedule.html:</b> The most intricate view page, dynamically generating cards representing each day of the selected month and year. The algorithm populates cards with stored database information, and users with 'manager' status can edit day-off settings, start and end hours. The day-off switch alters card appearance, changing background color to gray for designated days.

<h3>Technologies Used</h3>
Backend: Django<br>
Frontend: HTML, CSS, Javascript<br>
Database: SQLite<br>

Feel free to explore the application and provide feedback! If you have any questions or encounter issues, please reach out.
