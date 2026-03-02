from rest_framework.throttling import SimpleRateThrottle
import logging

logger = logging.getLogger(__name__)


class OrganizationRateThrottle(SimpleRateThrottle):
    scope = 'organization'

    def parse_rate(self, rate):
        """
        Support both standard DRF rates like '10/min'
        and custom second-based rates like '10/60s'.
        """
        logger.info(f"[Throttle] Parsing rate: {rate}")

        if rate is None:
            logger.warning("[Throttle] Rate is None")
            return (None, None)

        num, period = rate.split('/')
        num_requests = int(num)

        # Custom format: '<seconds>s'
        if period.endswith('s') and period[:-1].isdigit():
            duration = int(period[:-1])
        else:
            duration_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
            duration = duration_map.get(period[0])

        logger.info(f"[Throttle] Parsed -> num_requests={num_requests}, duration={duration}")

        return num_requests, duration

    def get_cache_key(self, request, view):
        """
        Unique cache key per organization + user.
        """
        if not request.user.is_authenticated:
            logger.info("[Throttle] Anonymous user — skipping throttle")
            return None

        profile = getattr(request.user, 'userprofile', None)

        if not profile:
            logger.warning("[Throttle] No userprofile found")
            return None

        if not profile.organization:
            logger.warning("[Throttle] User has no organization")
            return None

        org = profile.organization

        cache_key = f"throttle_org_{org.id}_user_{request.user.id}"
        logger.info(f"[Throttle] Cache key generated: {cache_key}")

        return cache_key

    def allow_request(self, request, view):
        """
        Dynamically compute rate from organization.
        """
        logger.info("========== Throttle Check Started ==========")

        if not request.user.is_authenticated:
            logger.info("[Throttle] Not authenticated — allowed")
            return True

        profile = getattr(request.user, 'userprofile', None)

        if not profile or not profile.organization:
            logger.info("[Throttle] No profile/org — allowed")
            return True

        org = profile.organization

        logger.info(
            f"[Throttle] Org={org.name}, "
            f"MaxRequests={org.max_requests}, "
            f"Window={org.time_window}s"
        )

        try:
            max_req = int(org.max_requests)
            window = int(org.time_window)
        except (TypeError, ValueError):
            logger.error("[Throttle] Invalid max_requests/time_window")
            return True

        # IMPORTANT: Always add 's' because your DB window is seconds
        self.rate = f"{max_req}/{window}s"

        logger.info(f"[Throttle] Computed rate: {self.rate}")

        # Let DRF handle:
        # - parsing rate
        # - generating key
        # - checking history
        result = super().allow_request(request, view)

        logger.info(f"[Throttle] Allowed? {result}")

        # self.history is created by DRF after super call
        if hasattr(self, 'history'):
            logger.info(f"[Throttle] Request history: {self.history}")

        logger.info("========== Throttle Check End ==========")

        return result