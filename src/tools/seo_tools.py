"""
SEO and customer service tools for YouTube video packaging.
"""
from langchain.tools import tool


@tool
def generate_whatsapp_cta(user_intent: str = "general") -> str:
    """
    Generate WhatsApp call-to-action message for YouTube comments.

    This tool creates professional and engaging WhatsApp contact messages
    to guide potential customers to your business contact.

    Args:
        user_intent: Type of user inquiry (general, pricing, sample, technical, partnership)

    Returns:
        Formatted WhatsApp CTA message
    """
    whatsapp_number = "+1 (213) 275-7332"

    cta_templates = {
        "general": (
            "Thanks for watching! 🙌\n\n"
            f"If you're interested in learning more about our biopolymer materials, "
            f"please reach out to our team on WhatsApp: {whatsapp_number}\n\n"
            "We'd love to discuss how our solutions can help your project!"
        ),
        "pricing": (
            "Great question! 💰\n\n"
            "For detailed pricing information and bulk quotes, please contact our sales team on WhatsApp: "
            f"{whatsapp_number}\n\n"
            "We offer competitive pricing for research and commercial applications."
        ),
        "sample": (
            "Thanks for your interest in our samples! 🧪\n\n"
            "To request material samples, please reach out on WhatsApp: "
            f"{whatsapp_number}\n\n"
            "Our team will guide you through the sample request process."
        ),
        "technical": (
            "Excellent technical question! 📊\n\n"
            "For detailed technical specifications and application guidance, please contact our "
            f"technical team on WhatsApp: {whatsapp_number}\n\n"
            "Our engineers are ready to help optimize your material selection."
        ),
        "partnership": (
            "We're always open to collaboration! 🤝\n\n"
            "For partnership discussions and joint R&D opportunities, please reach out on WhatsApp: "
            f"{whatsapp_number}\n\n"
            "Let's explore how we can work together to advance biomaterial innovation."
        )
    }

    return cta_templates.get(user_intent, cta_templates["general"])


@tool
def get_safe_vocabulary(word: str) -> str:
    """
    Get safe alternative words for medical/sensitive terms.

    Use this tool to replace restricted words with platform-safe alternatives
    for YouTube/TikTok compliance.

    Args:
        word: Word to check or replace

    Returns:
        Safe alternative word or the original if already safe
    """
    safe_vocab = {
        "surgery": "procedure",
        "injection": "application",
        "implant": "material placement",
        "fillers": "biopolymer augmentation",
        "plastic surgery": "aesthetic procedure",
        "botox": "botulinum toxin type A",
        "dermal fillers": "facial volumizing biopolymers",
        "cosmetic surgery": "aesthetic medicine"
    }

    return safe_vocab.get(word.lower(), word)
