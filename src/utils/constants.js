
// https://stackoverflow.com/questions/6042007/how-to-get-the-host-url-using-javascript-from-the-current-page
var protocol = window.location.protocol;
var slashes = protocol.concat("//");
var host = slashes.concat(window.location.host);
if (window.location.port) {
    host = host.replace("3000", "8000")
}
const HOST = host.concat("/");
export const LOGIN_API = HOST + "api/user/login/";
export const REGISTER_API = HOST + "api/user/signup/";
export const POST_API = HOST + "api/post/";
export const AUTHOR_API = HOST + "api/user/author/";
export const CURRENT_USER_API = HOST + "api/user/author/current_user/";
export const FRIEND_API = HOST + "api/friend/my_friends/";
export const FRIEND_REQUEST_API = HOST + "api/friend/friend_request/";
export const FRIEND_BOOL = HOST + 'api/friend/if_friend/';
export const USERNAME_LIST = HOST + 'api/user/author/username_list/';