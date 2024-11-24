from rest_framework.throttling import SimpleRateThrottle

class RoleBasedThrottle(SimpleRateThrottle):
    scope = 'role_based'

    def get_rate(self):
        """
        Define throttling rates based on user roles.
        """
        if self.user.is_authenticated:
            # Example role check: assuming roles are stored in a 'role' field
            if self.user.role == 'admin':
                return '10000/hour'  # Higher limit for admin users
            elif self.user.role == 'premium':
                return '5000/hour'  # Medium limit for premium users
            else:
                return '1000/hour'  # Default limit for regular users
        return '5/min'  # Default for anonymous users

    def get_cache_key(self, request, view):
        """
        Generate a unique cache key based on the user or IP.
        """
        if request.user.is_authenticated:
            return f"throttle_{self.scope}_{request.user.id}"
        return self.get_ident(request)  # Default: use IP for anonymous users