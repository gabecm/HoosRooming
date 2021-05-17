# HoosRooming
HoosRooming is a Django web application that helps UVa students find potential roommates.

## Features
* Profile Page
    * Displays name, phone number, profile picture, favorite spotify track and etc.
    * Should be the first page you're directed to after logging in
    * Try connecting your spotify account by clicking on the "Connect to Spotify" button
* Preferences Form
    * Allows the user to enter their roommate preferences (noise level, cleanliness level, budget, lease duration, etc.)
    * Please click on "Edit Preferences" when first logging in
* Matches Page
    * Displays your potential matches in order of highest to lowest compatibility 
    * Uses a distance algorithm to determine how compatible you are with other users based on your preferences
    * You may view the preferences of other users
    * You can accept and reject potential matches
        * Matches you accept are displayed in Pending Matches tab
    * Please accept the user Gabriel Mallari (with Pikachu profile picture) in order to test the messages feature.
    * Users who you accept and accept you back appear in Accepted Matches tab
        * Displays contact information like phone number and email
        * You may also start a conversation with using the app's direct messaging feature
            * Please click on the "Message" button under Gabriel's profile
* Messages Page
    * User-to-user messaging system with matched users
    * The left list displays all current chats in order to most recently received or sent messages
    * The right side displays the conversation of the user currently selected
    
## License 
The BSD License

Copyright (c) 2021 HoosRooming

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
