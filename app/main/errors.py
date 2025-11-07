from flask import render_template

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(e):
        return render_template("errors.html", error_code=404, error_message="Page not found."), 404

    @app.errorhandler(403)
    def forbidden_error(e):
        return render_template("errors.html", error_code=403, error_message="Access forbidden."), 403

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("errors.html", error_code=500, error_message="Internal server error."), 500

    @app.errorhandler(429)
    def too_many_requests(e):
        return render_template("errors.html", error_code=429, error_message="Too many requests, please try again later."), 429
