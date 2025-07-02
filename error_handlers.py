from flask import render_template, request, current_app, jsonify
from werkzeug.exceptions import HTTPException
from security_utils import SecurityUtils
import logging
import traceback

def register_error_handlers(app):
    """Register secure error handlers for the application"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Handle bad request errors"""
        SecurityUtils.log_security_event('BAD_REQUEST', str(error))
        
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'طلب غير صحيح',
                'error_code': 400
            }), 400
        
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """Handle unauthorized access errors"""
        SecurityUtils.log_security_event('UNAUTHORIZED_ACCESS', 
                                        f'Unauthorized access attempt from {request.remote_addr}')
        
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'غير مخول للوصول',
                'error_code': 401
            }), 401
        
        return render_template('errors/401.html'), 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle forbidden access errors"""
        SecurityUtils.log_security_event('FORBIDDEN_ACCESS', 
                                        f'Forbidden access attempt from {request.remote_addr}')
        
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'الوصول مرفوض',
                'error_code': 403
            }), 403
        
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle not found errors"""
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'الصفحة غير موجودة',
                'error_code': 404
            }), 404
        
        return render_template('404.html'), 404
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """Handle method not allowed errors"""
        SecurityUtils.log_security_event('METHOD_NOT_ALLOWED', 
                                        f'Method {request.method} not allowed for {request.url}')
        
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'طريقة الطلب غير مسموحة',
                'error_code': 405
            }), 405
        
        return render_template('errors/405.html'), 405
    
    @app.errorhandler(413)
    def payload_too_large_error(error):
        """Handle payload too large errors"""
        SecurityUtils.log_security_event('PAYLOAD_TOO_LARGE', 
                                        f'Large payload from {request.remote_addr}')
        
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'حجم البيانات كبير جداً',
                'error_code': 413
            }), 413
        
        return render_template('errors/413.html'), 413
    
    @app.errorhandler(429)
    def too_many_requests_error(error):
        """Handle too many requests errors"""
        SecurityUtils.log_security_event('RATE_LIMIT_EXCEEDED', 
                                        f'Rate limit exceeded from {request.remote_addr}')
        
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'تم تجاوز حد الطلبات المسموح. يرجى المحاولة لاحقاً',
                'error_code': 429
            }), 429
        
        return render_template('errors/429.html'), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors"""
        # Log the actual error for developers (but don't expose to users)
        current_app.logger.error(f'Server Error: {error}')
        current_app.logger.error(traceback.format_exc())
        
        # Log security event
        SecurityUtils.log_security_event('SERVER_ERROR', 
                                        f'Internal server error from {request.remote_addr}')
        
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'حدث خطأ في النظام. يرجى المحاولة لاحقاً',
                'error_code': 500
            }), 500
        
        return render_template('500.html'), 500
    
    @app.errorhandler(502)
    def bad_gateway_error(error):
        """Handle bad gateway errors"""
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'خطأ في الاتصال بالخدمة',
                'error_code': 502
            }), 502
        
        return render_template('errors/502.html'), 502
    
    @app.errorhandler(503)
    def service_unavailable_error(error):
        """Handle service unavailable errors"""
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'الخدمة غير متاحة حالياً',
                'error_code': 503
            }), 503
        
        return render_template('errors/503.html'), 503
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle all unhandled exceptions"""
        # Log the exception
        current_app.logger.error(f'Unhandled Exception: {e}')
        current_app.logger.error(traceback.format_exc())
        
        # Log security event
        SecurityUtils.log_security_event('UNHANDLED_EXCEPTION', 
                                        f'Unhandled exception from {request.remote_addr}: {str(e)}')
        
        # Pass through HTTP errors
        if isinstance(e, HTTPException):
            return e
        
        # Handle non-HTTP exceptions
        if request.is_json:
            return jsonify({
                'success': False,
                'message': 'حدث خطأ غير متوقع',
                'error_code': 500
            }), 500
        
        return render_template('500.html'), 500