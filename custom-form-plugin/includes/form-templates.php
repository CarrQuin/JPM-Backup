<?php
/**
 * 密码找回表单展示
 */
function cuf_display_password_reset_form() {
    ob_start(); ?>
    <form method="POST" class="cuf-form">
        <label>邮箱<span class="required">*</span></label>
        <input type="email" name="email" required>

        <button type="submit" name="cuf_reset_submit">发送重置链接</button>
    </form>
    <?php return ob_get_clean();
}

/**
 * 用户信息更新表单展示
 */
function cuf_display_user_info_form() {
    if (!is_user_logged_in()) {
        return '<div class="cuf-error">您需要登录才能更新信息。</div>';
    }

    $current_user = wp_get_current_user();
    ob_start(); ?>
    <form method="POST" class="cuf-form">
        <label>邮箱<span class="required">*</span></label>
        <input type="email" name="email" value="<?php echo esc_attr($current_user->user_email); ?>" required>

        <label>昵称</label>
        <input type="text" name="nickname" value="<?php echo esc_attr($current_user->nickname); ?>">

        <button type="submit" name="cuf_user_update_submit">更新信息</button>
    </form>
    <?php return ob_get_clean();
}
