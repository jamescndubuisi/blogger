# # # blog/utils/gemini_client.py
# # import os
# # from typing import Optional
# # from blogger.settings import GEMINI_API_KEY
# #
# # # The official example shows using `genai` client from Google SDK:
# # # from google import genai
# # # client = genai.Client()
# # # resp = client.models.generate_content(model="gemini-2.5-flash", contents="...")
# #
# # try:
# #     from google import genai
# # except Exception:
# #     genai = None
# #
# # GEMINI_API_KEY = GEMINI_API_KEY
# # GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
# #
# #
# # def generate_article_text(title: str, description: Optional[str] = None, word_target: int = 800) -> str:
# #     """
# #     Generate article text using Gemini.
# #     Returns generated string on success or raises RuntimeError on failure.
# #
# #     The function asks Gemini to produce a structured article: intro, multiple headings,
# #     and a short conclusion. It does NOT publish the article — result is returned for admin/editor review.
# #     """
# #     if genai is None:
# #         raise RuntimeError("Google Gemni SDK not installed. Please `pip install google-generativeai`")
# #
# #     if not GEMINI_API_KEY:
# #         raise RuntimeError("GEMINI_API_KEY not set in environment.")
# #
# #     prompt = (
# #         f"Write a detailed, professional blog article for the following title:\n\n"
# #         f"Title: {title}\n"
# #     )
# #     if description:
# #         prompt += f"Short guidance: {description}\n\n"
# #     prompt += (
# #         f"Requirements:\n"
# #         f"- Length: around {word_target} words (approximately)\n"
# #         f"- Structure: short introduction, 3–6 subheadings/sections (with short paragraphs), and a brief conclusion\n"
# #         f"- Include practical examples or bullet points where relevant\n"
# #         f"- Tone: clear, helpful, and professional; avoid mentioning that it was AI-generated\n\n"
# #         f"Return only the article content (no commentary)."
# #     )
# #
# #     # Initialize client with API key (the client automatically picks up env var in many SDKs,
# #     # but we'll pass it if the SDK supports passing key)
# #     try:
# #         # Some SDK versions pick up env var automatically; passing key if supported is safer.
# #         client = genai.Client(api_key=GEMINI_API_KEY) if hasattr(genai, "Client") else genai.Client()
# #     except TypeError:
# #         # fallback: instantiate without argument
# #         client = genai.Client()
# #
# #     # Call the model
# #     try:
# #         response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
# #     except Exception as e:
# #         raise RuntimeError(f"Gemini API call failed: {e}")
# #
# #     # response object shape may vary by SDK version; try common attributes
# #     text = getattr(response, "text", None)
# #     if text:
# #         return text
# #
# #     # Some SDKs return output structure
# #     try:
# #         # e.g. response.output[0].content[0].text
# #         out = response.output
# #         if out and isinstance(out, (list, tuple)):
# #             first = out[0]
# #             content = getattr(first, "content", None)
# #             if content and isinstance(content, (list, tuple)):
# #                 piece = content[0]
# #                 t = getattr(piece, "text", None)
# #                 if t:
# #                     return t
# #     except Exception:
# #         pass
# #
# #     # As a last resort, try str()
# #     result = str(response)
# #     if result:
# #         return result
# #
# #     raise RuntimeError("Unable to parse Gemini response.")
#
#
# # blog/utils/gemini_client.py
# # import os
# # from typing import Optional
# # from django.conf import settings
# # from blogger.settings import GEMINI_API_KEY
# #
# # # GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or getattr(settings, "GEMINI_API_KEY", "")
# # GEMINI_API_KEY = GEMINI_API_KEY
# # GEMINI_MODEL = os.environ.get("GEMINI_MODEL", getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash"))
#
# import os
# from typing import Optional
# from django.conf import settings
# import environ
#
# # Read the API key safely: prefer environment variable, fall back to Django settings
# env = environ.Env()
# environ.Env.read_env()
#
# # GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or getattr(settings, "GEMINI_API_KEY", "")
# GEMINI_API_KEY = env('GOOGLE_API')
# GEMINI_MODEL = os.environ.get("GEMINI_MODEL", getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash"))
#
#
#
# # Try to import recommended modern SDK first
# genai = None
# try:
#     # new official package: google-genai exposes module at `google.genai`
#     from google import genai as _genai_mod
#     genai = _genai_mod
# except Exception:
#     try:
#         # some older guides used 'google.generativeai'
#         import google.generativeai as _gen_old
#         genai = _gen_old
#     except Exception:
#         genai = None
#
#
# def generate_article_text(title: str, description: Optional[str] = None, word_target: int = 800) -> str:
#     """
#     Generate article text using Gemini (Google GenAI). Returns the generated text.
#     Raises RuntimeError with clear messages on error.
#     """
#     if genai is None:
#         raise RuntimeError(
#             "Google GenAI SDK not installed. Run `pip install google-genai` (recommended) "
#             "or `pip install google-generativeai` and restart the server."
#         )
#
#     if not GEMINI_API_KEY:
#         raise RuntimeError("GEMINI_API_KEY not set in environment. Set it and restart your server.")
#
#     prompt = (
#         f"Write a professional blog article for the following title.\n\n"
#         f"Title: {title}\n"
#     )
#     if description:
#         prompt += f"Guidance: {description}\n\n"
#     prompt += (
#         f"Requirements:\n"
#         f"- ~{word_target} words\n"
#         f"- short introduction, 3–6 subheadings, short paragraphs, examples where relevant\n"
#         f"- tone: helpful and professional\n\n"
#         f"Return only the article text.\n"
#     )
#
#     # Different SDKs have slightly different client APIs — try common patterns.
#     try:
#         # modern google-genai usage: from google import genai; client = genai.Client(); client.models.generate_content(...)
#         if hasattr(genai, "Client"):
#             client = genai.Client(api_key=GEMINI_API_KEY) if "Client" in dir(genai) else genai.Client()
#             try:
#                 response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
#             except TypeError:
#                 # some versions use generate_content(... ) with a list or different param names
#                 response = client.models.generate_content(model=GEMINI_MODEL, content=prompt)
#             # prefer .text if available
#             text = getattr(response, "text", None)
#             if text:
#                 return text
#             # sometimes at response.output[0].content[0].text
#             out = getattr(response, "output", None)
#             if out and isinstance(out, (list, tuple)) and len(out) > 0:
#                 first = out[0]
#                 content = getattr(first, "content", None)
#                 if content and isinstance(content, (list, tuple)) and len(content) > 0:
#                     maybe = getattr(content[0], "text", None) or content[0]
#                     return str(maybe)
#             return str(response)
#
#         # legacy google.generativeai usage
#         if hasattr(genai, "generate"):
#             # example older usage: genai.configure(api_key=...)
#             try:
#                 genai.configure(api_key=GEMINI_API_KEY)
#             except Exception:
#                 pass
#             resp = genai.generate(model=GEMINI_MODEL, prompt=prompt)
#             # older libs might return dict-like
#             if isinstance(resp, dict):
#                 return resp.get("output", "") or str(resp)
#             return str(resp)
#
#     except Exception as e:
#         raise RuntimeError(f"Gemini API call failed: {e}")
#
#     # fallback
#     raise RuntimeError("Unable to generate content (unhandled response shape).")


# blog/utils/gemini_client.py
import os
import logging
from typing import Optional, Dict, Any
from django.conf import settings
from django.core.cache import cache
import environ

logger = logging.getLogger(__name__)

# Environment setup
env = environ.Env()
environ.Env.read_env()

# Configuration
GEMINI_API_KEY = env('GOOGLE_API', default=os.environ.get('GOOGLE_API', ''))
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash"))
GEMINI_TIMEOUT = int(os.environ.get("GEMINI_TIMEOUT", "30"))  # 30 seconds default

# Try to import Gemini SDK
genai = None
sdk_type = None

try:
    # Try modern google-genai first
    from google import genai as _genai_mod

    genai = _genai_mod
    sdk_type = "modern"
    logger.info("Using modern google-genai SDK")
except ImportError:
    try:
        # Fallback to google-generativeai
        import google.generativeai as _gen_old

        genai = _gen_old
        sdk_type = "legacy"
        logger.info("Using legacy google-generativeai SDK")
    except ImportError:
        genai = None
        sdk_type = None
        logger.warning("No Gemini SDK found")


class GeminiError(Exception):
    """Custom exception for Gemini-related errors"""
    pass


class GeminiClient:
    """Enhanced Gemini client with better error handling and caching"""

    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.model = GEMINI_MODEL
        self.timeout = GEMINI_TIMEOUT
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Gemini client based on available SDK"""
        if not genai:
            raise GeminiError(
                "Google GenAI SDK not installed. Install with:\n"
                "pip install google-genai (recommended) or pip install google-generativeai"
            )

        if not self.api_key:
            raise GeminiError(
                "GEMINI_API_KEY not configured. Set GOOGLE_API environment variable."
            )

        try:
            if sdk_type == "modern":
                self.client = genai.Client(api_key=self.api_key)
            elif sdk_type == "legacy":
                genai.configure(api_key=self.api_key)
                self.client = genai

            logger.info(f"Gemini client initialized with {sdk_type} SDK")

        except Exception as e:
            raise GeminiError(f"Failed to initialize Gemini client: {str(e)}")

    def _generate_cache_key(self, title: str, description: str, word_target: int) -> str:
        """Generate cache key for the request"""
        import hashlib
        content = f"{title}|{description or ''}|{word_target}|{self.model}"
        return f"gemini_article_{hashlib.md5(content.encode()).hexdigest()}"

    def _build_prompt(self, title: str, description: Optional[str] = None,
                      word_target: int = 800) -> str:
        """Build optimized prompt for article generation"""
        prompt_parts = [
            "You are a professional content writer. Write a high-quality blog article with the following specifications:",
            f"\nTitle: {title}",
        ]

        if description:
            prompt_parts.append(f"Focus/Guidance: {description}")

        prompt_parts.extend([
            f"\nRequirements:",
            f"- Target length: approximately {word_target} words",
            f"- Structure: engaging introduction, 3-6 well-organized sections with descriptive subheadings, and a concise conclusion",
            f"- Writing style: professional, informative, and engaging",
            f"- Include practical examples, actionable insights, or relevant details where appropriate",
            f"- Use proper formatting with clear headings (use ## for main sections)",
            f"- Avoid mentioning AI generation or similar meta-commentary and do not use # symbol",
            f"- Focus on providing genuine value to readers",
            f"\nReturn only the article content with proper markdown formatting."
        ])

        return "\n".join(prompt_parts)

    def _call_modern_api(self, prompt: str) -> str:
        """Call modern google-genai API"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            # Extract text from response
            if hasattr(response, 'text') and response.text:
                return response.text

            # Try alternative response structures
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        return candidate.content.parts[0].text

            # Fallback to string representation
            text = str(response)
            if text and len(text) > 50:  # Ensure it's actual content
                return text

            raise GeminiError("Unable to extract text from API response")

        except Exception as e:
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                raise GeminiError("API quota exceeded. Please try again later or check your billing.")
            elif "api key" in str(e).lower() or "auth" in str(e).lower():
                raise GeminiError("Authentication failed. Please check your API key.")
            else:
                raise GeminiError(f"API call failed: {str(e)}")

    def _call_legacy_api(self, prompt: str) -> str:
        """Call legacy google-generativeai API"""
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)

            if hasattr(response, 'text') and response.text:
                return response.text

            # Try accessing through candidates
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content'):
                    return candidate.content.parts[0].text

            raise GeminiError("Unable to extract text from legacy API response")

        except Exception as e:
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                raise GeminiError("API quota exceeded. Please try again later or check your billing.")
            elif "api key" in str(e).lower() or "auth" in str(e).lower():
                raise GeminiError("Authentication failed. Please check your API key.")
            else:
                raise GeminiError(f"Legacy API call failed: {str(e)}")

    def generate_content(self, title: str, description: Optional[str] = None,
                         word_target: int = 800, use_cache: bool = True) -> str:
        """
        Generate article content using Gemini AI

        Args:
            title: Article title (required)
            description: Optional description or guidance
            word_target: Target word count (default: 800)
            use_cache: Whether to use caching (default: True)

        Returns:
            Generated article content as string

        Raises:
            GeminiError: If generation fails
        """
        if not title or not title.strip():
            raise GeminiError("Title is required for article generation")

        # Check cache first
        cache_key = None
        if use_cache:
            cache_key = self._generate_cache_key(title, description or "", word_target)
            cached_content = cache.get(cache_key)
            if cached_content:
                logger.info(f"Returning cached content for: {title}")
                return cached_content

        # Build prompt
        prompt = self._build_prompt(title.strip(), description, word_target)

        # Generate content
        try:
            if sdk_type == "modern":
                content = self._call_modern_api(prompt)
            elif sdk_type == "legacy":
                content = self._call_legacy_api(prompt)
            else:
                raise GeminiError("No valid SDK available")

            # Validate content
            if not content or len(content.strip()) < 100:
                raise GeminiError("Generated content is too short or empty")

            # Cache the result for 24 hours
            if use_cache and cache_key:
                cache.set(cache_key, content, 60 * 60 * 24)
                logger.info(f"Cached generated content for: {title}")

            logger.info(f"Successfully generated {len(content.split())} words for: {title}")
            return content.strip()

        except GeminiError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error generating content for '{title}': {str(e)}")
            raise GeminiError(f"Unexpected generation error: {str(e)}")


# Global client instance
_client = None


def get_gemini_client() -> GeminiClient:
    """Get or create global Gemini client instance"""
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client


def generate_article_text(title: str, description: Optional[str] = None,
                          word_target: int = 800) -> str:
    """
    Generate article text using Gemini (backward compatibility function)

    Args:
        title: Article title
        description: Optional description or guidance
        word_target: Target word count

    Returns:
        Generated article content

    Raises:
        RuntimeError: If generation fails (for backward compatibility)
    """
    try:
        client = get_gemini_client()
        return client.generate_content(title, description, word_target)
    except GeminiError as e:
        # Convert to RuntimeError for backward compatibility
        raise RuntimeError(str(e))


def test_gemini_connection() -> Dict[str, Any]:
    """
    Test Gemini connection and return status information

    Returns:
        Dictionary with connection status and details
    """
    try:
        client = get_gemini_client()

        # Try a simple generation
        test_content = client.generate_content(
            title="Test Article",
            description="A simple test to verify API connectivity",
            word_target=100,
            use_cache=False
        )

        return {
            "status": "success",
            "sdk_type": sdk_type,
            "model": client.model,
            "api_key_set": bool(client.api_key),
            "test_generation_length": len(test_content.split()),
            "message": "Gemini connection successful"
        }

    except Exception as e:
        return {
            "status": "error",
            "sdk_type": sdk_type,
            "api_key_set": bool(GEMINI_API_KEY),
            "error": str(e),
            "message": "Gemini connection failed"
        }


# Utility functions for admin
def clear_gemini_cache():
    """Clear all Gemini-related cache entries"""
    try:
        # This is a simple implementation - in production you might want
        # to use cache versioning or more sophisticated cache management
        cache.delete_many([key for key in cache._cache.keys() if key.startswith('gemini_')])
        return True
    except Exception:
        return False


def get_generation_stats() -> Dict[str, Any]:
    """Get statistics about Gemini generations (if tracking is implemented)"""
    # This could be expanded to track generation statistics
    # For now, return basic info
    return {
        "sdk_available": genai is not None,
        "sdk_type": sdk_type,
        "model": GEMINI_MODEL,
        "timeout": GEMINI_TIMEOUT,
        "cache_enabled": True
    }