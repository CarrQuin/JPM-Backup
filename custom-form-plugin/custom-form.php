<?php
/**
 * Plugin Name: Custom Form
 * Description: This is just a demo, may cause many bugs  
 * Version: 1.0
 * Author: Kaiyu Qian
 * Text Domain: custom-form
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Load the required classes and files
require_once plugin_dir_path(__FILE__) . 'includes/class-form-handler.php';
require_once plugin_dir_path(__FILE__) . 'includes/form-templates.php';

// Load the stylesheet
function cuf_enqueue_styles() {
    wp_enqueue_style('custom-user-forms-style', plugin_dir_url(__FILE__) . 'assets/styles.css');
}
add_action('wp_enqueue_scripts', 'cuf_enqueue_styles');

/**
 * Initialize form shortcodes
 */
function cuf_register_shortcodes() {
    add_shortcode('cuf_register_form', 'cuf_display_register_form');
    add_shortcode('cuf_login_form', 'cuf_display_login_form');
    add_shortcode('cuf_password_reset_form', 'cuf_display_password_reset_form');
    add_shortcode('cuf_user_info_form', 'cuf_display_user_info_form');
}
add_action('init', 'cuf_register_shortcodes');
