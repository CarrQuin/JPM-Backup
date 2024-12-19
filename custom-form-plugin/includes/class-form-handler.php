<?php
// Form handler class
// 表单处理类
class CUF_Form_Handler {
    /**
     * Handle registration form submissions
     * 处理注册表单提交
     */
    public static function handle_register_form() {
        if (isset($_POST['cuf_register_submit'])) {
            $username = sanitize_text_field($_POST['username']);
            $email = sanitize_email($_POST['email']);
            $password = sanitize_text_field($_POST['password']);
            $errors = [];
    
            if (empty($username) || empty($email) || empty($password)) {
                $errors[] = 'All required fields must be filled out.'; // EN
            }
            if (!is_email($email)) {
                $errors[] = 'Invalid email format.'; // EN
            }
    
            // Check if the username or email already exists.
            // 检查用户名或邮箱是否已存在
            global $wpdb;
            $table_name = $wpdb->prefix . 'swpm_members_tbl';
            $existing_user = $wpdb->get_row($wpdb->prepare(
                "SELECT * FROM $table_name WHERE user_name = %s OR email = %s",
                $username,
                $email
            ));
    
            if ($existing_user) {
                $errors[] = 'The username or email already exists.';
            }
    
            // If there are no errors, write to the SWPM database.
            // 如果没有错误，写入 SWPM 数据库
            if (empty($errors)) {
                $wpdb->insert($table_name, [
                    'user_name'        => $username,
                    'email'            => $email,
                    'password'         => wp_hash_password($password),
                    'membership_level' => 2, // Default membership level, 默认会员级别
                    'account_state'    => 'active', // Active status, 激活状态
                    'first_name'       => '',
                    'last_name'        => '',
                ]);
    
                echo '<div class="cuf-success">Registration successful </div>'; // EN
            } else {
                foreach ($errors as $error) {
                    echo '<div class="cuf-error">' . esc_html($error) . '</div>';
                }
            }
        }
    }

    /**
     * Handle password recovery form submissions.
     * 处理密码找回表单提交
     */
    public static function handle_password_reset_form() {
        if (isset($_POST['cuf_reset_submit'])) {
            $email = sanitize_email($_POST['email']);
            if (empty($email) || !is_email($email)) {
                echo '<div class="cuf-error">请输入有效的电子邮箱地址！</div>';
                return;
            }

            $user = get_user_by('email', $email);
            if ($user) {
                $reset_link = wp_lostpassword_url();
                echo '<div class="cuf-success">密码重置链接已发送，请检查您的邮箱！</div>';
            } else {
                echo '<div class="cuf-error">此邮箱未注册。</div>';
            }
        }
    }

    /**
     * 处理用户信息更新
     */
    public static function handle_user_info_update() {
        if (isset($_POST['cuf_user_update_submit']) && is_user_logged_in()) {
            $user_id = get_current_user_id();
            $email = sanitize_email($_POST['email']);
            $nickname = sanitize_text_field($_POST['nickname']);
            $errors = [];
    
            if (!is_email($email)) {
                $errors[] = '无效的电子邮箱格式！';
            }
    
            // 更新 Simple Membership 数据库
            if (empty($errors)) {
                global $wpdb;
                $table_name = $wpdb->prefix . 'swpm_members_tbl';
    
                $wpdb->update($table_name, [
                    'email' => $email,
                    'nickname' => $nickname,
                ], [
                    'user_id' => $user_id,
                ]);
    
                echo '<div class="cuf-success">用户信息已更新！</div>';
            } else {
                foreach ($errors as $error) {
                    echo '<div class="cuf-error">' . esc_html($error) . '</div>';
                }
            }
        }
    }
}
// 处理表单提交的挂钩
add_action('init', ['CUF_Form_Handler', 'handle_register_form']);
add_action('init', ['CUF_Form_Handler', 'handle_password_reset_form']);
add_action('init', ['CUF_Form_Handler', 'handle_user_info_update']);
