# Best Pets API

## Introduction
Best Pets API is a Django REST Framework application designed to provide the back-end functionality for the [Best Pets front-end React application](https://github.com/Roybin0/best-pets). It offers a set of APIs to handle user authentication, pet profiles, pet tales, and other related features. 

The link to the deployed API can be found [here](https://bestpets-api.herokuapp.com/) and you can find the full list of User Stories on our Project Board: [Best Pets](https://github.com/users/Roybin0/projects/6/views/1).

This README provides an overview of the API and outlines the deployment process.

## Table of Contents
1. [Deployment](#deployment)
2. [User Authentication](#user-authentication)
3. [API Endpoints](#api-endpoints)
4. [Manual Testing](#manual-testing)
5. [Credits](#credits)
6. [Acknowledgements](#acknowledgements)

## Deployment
To deploy the Best Pets API locally, follow these steps:

1. Clone the repository: `git clone https://github.com/your/repository.git`
2. Install the necessary dependencies: `pip install -r requirements.txt`
3. Set up the database:
   - Create a new PostgreSQL database.
   - Update the database configuration in the settings file.
   - Run the migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`
5. The API will be available at `http://localhost:8000/`.

## User Authentication
The Best Pets API uses [dj-rest-auth](https://dj-rest-auth.readthedocs.io/) for user authentication. It provides a set of endpoints for user registration, login, logout, password reset, and more. 

- `POST /bestpets-api.herokuapp.com/api-auth/login/` - Log in an existing user.
- `POST /bestpets-api.herokuapp.com/api-auth/logout/` - Log out the currently authenticated user.

For more information on how to use dj-rest-auth, refer to the [documentation](https://dj-rest-auth.readthedocs.io/).

## API Endpoints
The Best Pets API offers the following main endpoints:

- `/bestpets-api.herokuapp.com/pets/` - Endpoint for creating and managing pet profiles.
- `/bestpets-api.herokuapp.com/pettales/` - Endpoint for creating and managing pet tales.
- `/bestpets-api.herokuapp.com/petpics/` - Endpoint for creating and managing pet pics.
- `/bestpets-api.herokuapp.com/owners/` - Endpoint for creating and managing pet owner profiles.
- `/bestpets-api.herokuapp.com/followers-owners/` - Endpoint related to followers of other users.
- `/bestpets-api.herokuapp.com/followers-pets/` - Endpoint related to followers of pets.
- `/bestpets-api.herokuapp.com/comments/` - Endpoint for creating and managing comments.
- `/bestpets-api.herokuapp.com/likes/` - Endpoint for creating and managing likes.

For detailed information about each endpoint, including request/response formats and required authentication, refer to the API documentation or explore the codebase.

## Manual Testing
Basic manual testing has been carried out to ensure the functionality of the Best Pets API. The following areas have been tested:

1. User Registration and Login:
   - Registering a new user.
   - Logging in with valid credentials.
   - Logging in with invalid credentials.
   - Logging out.

2. Pet Profiles:
   - Creating a new pet profile.
   - Retrieving a list of pet profiles.
   - Updating and deleting a pet profile.

3. Pet Tales:
   - Creating a new pet tale.
   - Retrieving a list of pet tales.
   - Updating and deleting a pet tale.

4. Likes and Comments:
   - Liking and unliking content.
   - Adding a comment to a pet tale.
   - Editing and deleting comments.

## Credits
The Best Pets API was inspired by Code Institute's [DRF API tutorial](https://github.com/Code-Institute-Solutions/drf-api). It was built using Django REST Framework and incorporates various libraries and tools to handle user authentication, data storage, and API functionality.

## Acknowledgements
Special thanks to Charlotte and Carolann for their support and assistance during the development of the Best Pets API. Many thanks to everyone who supplied endless images of their pets!
