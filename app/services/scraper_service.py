"""Job scraping service for extracting job descriptions from URLs."""

import re

from bs4 import BeautifulSoup


class JobScraperService:
    """Service for scraping job postings from various platforms."""

    @staticmethod
    def extract_job_description(html_content: str, url: str) -> str | None:
        """
        Extract job description from HTML content.

        Args:
            html_content: Raw HTML content from the job posting
            url: Original URL (used to determine platform)

        Returns:
            Cleaned job description text or None if extraction fails
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.decompose()

        # Platform-specific extraction
        if "linkedin.com" in url.lower():
            return JobScraperService._extract_linkedin(soup)
        elif "indeed.com" in url.lower():
            return JobScraperService._extract_indeed(soup)
        elif "greenhouse.io" in url.lower():
            return JobScraperService._extract_greenhouse(soup)
        elif "lever.co" in url.lower():
            return JobScraperService._extract_lever(soup)
        else:
            # Generic extraction
            return JobScraperService._extract_generic(soup)

    @staticmethod
    def _extract_linkedin(soup: BeautifulSoup) -> str | None:
        """Extract from LinkedIn job postings."""
        # LinkedIn job description container
        selectors = [
            "div.description__text",
            "div.show-more-less-html__markup",
            'div[class*="description"]',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return JobScraperService._clean_text(element.get_text())

        return None

    @staticmethod
    def _extract_indeed(soup: BeautifulSoup) -> str | None:
        """Extract from Indeed job postings."""
        selectors = [
            "div#jobDescriptionText",
            "div.jobsearch-jobDescriptionText",
            'div[id*="description"]',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return JobScraperService._clean_text(element.get_text())

        return None

    @staticmethod
    def _extract_greenhouse(soup: BeautifulSoup) -> str | None:
        """Extract from Greenhouse job boards."""
        selectors = [
            "div#content",
            "div.content",
            'div[class*="description"]',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return JobScraperService._clean_text(element.get_text())

        return None

    @staticmethod
    def _extract_lever(soup: BeautifulSoup) -> str | None:
        """Extract from Lever job boards."""
        selectors = [
            "div.section-wrapper",
            "div.posting-description",
            'div[class*="description"]',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return JobScraperService._clean_text(element.get_text())

        return None

    @staticmethod
    def _extract_generic(soup: BeautifulSoup) -> str | None:
        """Generic extraction for unknown platforms."""
        # Try common container patterns
        selectors = [
            'div[class*="description"]',
            'div[id*="description"]',
            "article",
            "main",
            'div[class*="content"]',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = JobScraperService._clean_text(element.get_text())
                # Only return if it looks substantial
                if text and len(text) > 200:
                    return text

        # Fallback: get all text
        text = soup.get_text()
        return JobScraperService._clean_text(text) if len(text) > 200 else None

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove multiple newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate if URL looks like a job posting.

        Args:
            url: URL to validate

        Returns:
            True if URL appears valid
        """
        url_lower = url.lower()

        # Check if it's a URL
        if not url.startswith(("http://", "https://")):
            return False

        # Known job platforms
        job_platforms = [
            "linkedin.com/jobs",
            "indeed.com",
            "greenhouse.io",
            "lever.co",
            "workable.com",
            "smartrecruiters.com",
            "breezy.hr",
            "angel.co",
            "wellfound.com",
            "remoteok.com",
            "weworkremotely.com",
        ]

        return any(platform in url_lower for platform in job_platforms)
