<?php
/**
 * Customize the login/logout menu Login Link.
 * @param string $login_logout_menu_login The login link.
 * @return string The modified login link.
 */
function login_logout_menu_login_cb( $login_logout_menu_login ) {
	// 	return site_url( '/membership-login/' ) ;
		return home_url( '/membership-login/' );
}
add_filter( 'login_logout_menu_login', 'login_logout_menu_login_cb' );
	
/**
* Filter to redirect a user to a specific page after login.
* @return string login URL with page slug on which it will be redirected after login
*/
// function loginpress_login_menu_login_redirect() {
// 	return wp_login_url( home_url() );
// }
// add_filter( 'login_logout_menu_login', 'loginpress_login_menu_login_redirect' );
	
/**
 * The username in the greeting message.
 * @param string $username
 * @return string The customized message.
 */
function login_logout_menu_username_cb( $username ) {
		return 'Hi, ' . $username;
}
add_filter( 'login_logout_menu_username', 'login_logout_menu_username_cb' );
	
/**
* Filter to Change the user redirect URL
* @return string Custom link to user page
*/
	function loginpress_login_logout_menu_user_link() {
		// return site_url( '/membership-profile/' ) ;
		return home_url( '/membership-profile/' );
}
add_filter( 'login_logout_menu_username_url', 'loginpress_login_logout_menu_user_link' );
	
/**
 * Customize the login/logout menu register Link.
 * @return string The modified register link.
 */
function login_logout_menu_register_link(){
	// 	return site_url( /membership-registration/ ) ;
		return home_url('/membership-registration/') ;
}
add_filter( 'login_logout_menu_register', 'login_logout_menu_register_link' );
	
/**
 * Filter to redirect a user to a specific page after logout.
 * @return string logout URL with page slug on which it will be redirected after logout
 */
// function loginpress_login_menu_logout_redirect() {
// 	 return wp_logout_url( home_url());
// }
// add_filter( 'login_logout_menu_logout', 'loginpress_login_menu_logout_redirect' );
	
//-------------------------------------------------------------------------------------------------------
//-------------------------------------------------------------------------------------------------------