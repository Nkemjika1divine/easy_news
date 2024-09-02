### Users
- `POST /api/v1/users/register`: This registers a user to the application
- `PUT /api/v1/users/verify_email`: This verifies the user's email
- `POST /api/v1/users/confirm_password`: This is confirms the user's password
- `PUT /api/v1/users/change_password`: This changes the user's password
- `GET /api/v1/users/get_password_reset_token`: This sends the user a password reset token
- `PUT /api/v1/users/change_email`: This changes the user's email
- `GET /api/v1/users/profile`: This returns the users profile with the categories of news they follows and the channels they follow
- `PUT /api/v1/users/change_name`: This changes the user's name
- `PUT /api/v1/users/promote/{user_id}`: This upgrades a user to admin and can only be done by the superuser
- `PUT /api/v1/users/demote/{user_id}`: This demotes a user from admin and can only be done by the superuser
- `DELETE /api/v1/users/delete_my_account`: This allows users to delete their account
- `DELETE /api/v1/users/{user_id}`: This deletes a user's account and can only be done by admins and the superuser

### Categories
- `POST /api/v1/categories/add`: This adds a new category to the database and can only be done by admins and the superuser
- `PUT /api/v1/categories/{category_id}`: This edits a category name and can only be done by admins and the superuser
- `GET /api/v1/categories`: This returns all the categories in the database 
- `DELETE /api/v1/categories/{category_id}`: This deletes a category and can only be done by admins and the superuser

### Channels
- `POST /api/v1/channels/add`: This method adds a new channel to the database and can only be done by admins and the superuser
- `PUT /api/v1/channels/edit/{channel_id}`: This method edits a channel's information and can only be done by admins and the superuser
- `GET /api/v1/channels`: This returns all channels in the database
- `DELETE /api/v1/channels/{channel_id}`: This deletes a channel from the database

### User following channels
- `POST /api/v1/users/channels/add`: This allows a user to start following a channel
- `DELETE /api/v1/users/channels/remove/{channel_name}`: This stops a user from following a channel
- `GET /api/v1/users/channels/follows`: This returns all the channels a user follows

### User following categories
- `POST /api/v1/users/categories/add`: This allows a user to follow a news category
- `DELETE /api/v1/users/categories/remove{category_name}`: This stops a user from following a category of news
- `GET /api/v1/users/categories/all`: This returns all the categories a user follows