# Social media platform project
#### Video Demo:  
## Demonstration
Watch the [YouTube video](https://youtu.be/KHmCH-Hb_z0) to see the application in action.
## Description
Using Python (Django framework, models), JavaScript, HTML, and CSS, complete the implementation of a social media platform that allows users to make posts, follow other users, and *like* posts. 
You must login to use these features.
First you create an account and choose a username and password and upload an image for your proile(not mandatory)
then when you are loged in you can all posts thar were posted by the other users and like them and you can add your
own post (either text or photo or both) and the other users can see it also. when clicking on any name of the post creator 
you view the user's profile when you can see the number of user's followers and number of users who follows and you can
follow or un follow the user and see all his posts and by clicking on the photo you view it.
when you click on the link following you see all the posts of the users you follow.
when you click on any post you view the post and where you can make like also and see the post's comments and comment on the post and if you are the owner
of the post you have the ability to edit the text or photo and delet the post.
when viewing your profile(by clicking on the link of your name on the nav bar or by clicking on your name on a post of you) you can't
follow yourself and by clicking on your profile photo you view your image with a button to change your image or delete it.
and in the profile, following and all posts pages you can see ten posts for each page and you can go to other pages to see the remain posts(using Pagination).
- # Implementation
  * [Models](#models)
    + [User](#user)
    + [Post](#post)
    + [Comment](#comment)
    + [Like](#like)
    + [Following](#following)
  * [Views](#views)
    + [index](#index)
    + [add_post](#add_post)
    + [profile](#profile)
    + [edit_profile](#edit-profile)
    + [following](#following)
    + [follow](#follow)
    + [unfollow](#unfollow)
    + [delete_post](#delet_post)
    + [view_post](#view_post)
    + [add_comment](#add_comment)
    + [edit_image](#edit_image)
    + [edit_post_photo](#edit_post_photo)
    + [delete_profile_img](#delete_profile_img)
    + [delete_post_img](#delete_post_img)
    + [like_post](#like_post)
    + [unlike_post](#unlike_post)
    + [edit_post](#edit_post)
    + [login_view](#login-view)
    + [logout_view](#logout-view)
    + [register](#register)
## Models
### User
Contains User Model extension with additional fields.

Fields:
* image - user's profile photo

### Post 
Contains all post info.

Fields:
* user - who posted the post
* text - post's inner text
* post - post's image
* username - name of the user who posted the post
* date - post's publication date

### Comment
Contains all comment info.

Fields:
* user - who posted the comment
* post_id - the id of the post which is being commented
* comment - comment's  text
* date - comment's publication date

### Like 
Contains all like info.

Fields:
* user - who liked a post/comment
* post_id - the id of the post which is being commented

### Following 
Contains all who follows who info.

Fields:
* follower - user who is following
* following - user who is being followed

## Views
### index
Here you can:
* View all posts
* Like them (only for logged-in users)
* Create a new post (only for logged-in users)
* click on any post to view it
### add_post
(only for logged-in users)
Here you can:
* share new post(either text or image or both)

### profile
(only for logged-in users)

Here you can:
* View all user's posts
* Like them 
* Follow the user (if you are not this user)
* Click on profile image to view it(edit it if you are the owner)
* click on any post to view it

### edit_profile
(only for logged-in users)

Here you can:
* Change your *name*
* Change your *birthdate*
* Change your *about info*
* Change your *profile picture*
* Change your *country*

### following
(only for logged-in users)

Here you can:
* View all posts created by followed users
* Like them
* click on any post to view it

### follow
(only for logged-in users)

Controls following users (only POST method allowed).

### unfollow
(only for logged-in users)

Controls unfollowing users (only POST method allowed).

### delete post
(only for logged-in users)

Deleting post if you are the owner.

### view_post
(only for logged-in users)

* view the post conrent
* view the comments 
* adding new comment 
* edit the caption (only if you are the owner of the post)
* edit the post image (only if you are the owner of the post)
* delet the post (only if you are the owner of the post)

### add_comment
(only for logged-in users)
* adding new comment

### edit_image
(only for logged-in users)
* edit the profile image

### edit_post_photo
(only for logged-in users)
* edit the post image

### delete_profile_img
(only for logged-in users)
* delete the profile image

### delete_post_img
(only for logged-in users)
* delete the post image

## like_post
(only for logged-in users)
* like post using API

## unlike_post
(only for logged-in users)
* unlike post using API

## edit_post
(only for logged-in users)
* edit the text of a post using API

### login_view
Controls logging in.

### logout_view
Controls logging out.

### register
Controls registration.

