Django Web Application for Restaurant Employee Scheduling
Overview
This web application was developed to address the need for efficient employee schedule management in a restaurant setting. As the manager of a restaurant, I faced challenges in keeping track of the schedules, and this project stems from a desire to create a solution based on my firsthand experience and daily operational needs.

The application not only fulfills the technical complexity requirements but also prioritizes a user-friendly experience. Utilizing Django with three distinct models and integrating Javascript for seamless database updates, the project goes beyond the mere creation of models. Every aspect, from buttons to styles, borders, and cards, has been meticulously designed to enhance usability, responsiveness, and visual appeal.

Project Structure
Files in chefiapp
Layout.html: Centralizes basic information for the header and footer, utilized across all other templates.

Index.html: Serves as the 'home' page, welcoming users after logging in and acting as the main gateway to the application.

login.html: Allows users to log in or navigate to the registration page.

register.html: Enables users to create an account for accessing the web application.

profile.html: Provides users with access to basic personal information and the ability to make necessary updates. User profiles can be viewed by others simply by using the user's ID in the URL.

staff.html: Displays cards for all users, showcasing their names, job descriptions, and links to their schedules. All users can view staff details and schedules, but only users with 'manager' status can edit profile and schedule data.

schedule.html: The most intricate view page, dynamically generating cards representing each day of the selected month and year. The algorithm populates cards with stored database information, and users with 'manager' status can edit day-off settings, start and end hours. The day-off switch alters card appearance, changing background color to gray for designated days.

Usage
Profile Editing: Users can view and edit their profiles, with managers having the additional ability to edit staff profiles.

Staff Viewing: All users can view staff details and navigate to individual profiles and schedules.

Schedule Management: Managers can edit schedules, setting day-offs or modifying working hours for each staff member on specific days.

Technologies Used
Backend: Django
Frontend: HTML, CSS, Javascript
Database: SQLite
Feel free to explore the application and provide feedback! If you have any questions or encounter issues, please reach out.
