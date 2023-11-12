def head_tag_generator(title="Flask-Imp", static_endpoint="static", no_js=False):
    """Generate the head tag for the HTML template files."""

    js = (f'<script defer src=\"{{{{ url_for(\'{static_endpoint}\', '
          f'filename=\'js/main.js\') }}}}\"></script>') if not no_js else ""

    return f"""\
{{#    https://github.com/joshbuchea/HEAD #}}

    <title>{{% block title %}}{{% endblock %}}{title}</title>
    <base href="{{{{ request.base_url }}}}">

    <!-- Security -->
{{#    <meta http-equiv="Content-Security-Policy" content="script-src 'self' 'unsafe-inline' 'unsafe-eval';">#}}

    <!-- Bots -->
    <meta name="robots" content="index,follow">
    <meta name="googlebot" content="index,follow">

    <!-- General Settings -->
    <meta charset="utf-8">
    <meta http-equiv="x-dns-prefetch-control" content="off">
    <meta name="google" content="nositelinkssearchbox">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="msapplication-TileColor" content="#da532c">
    <meta name="theme-color" content="#ffffff">
    <meta name=”rating” content=”general”>
    <meta name="referrer" content="no-referrer">
    <meta name="format-detection" content="telephone=no">

    <!-- GEO location -->
    <meta name="ICBM" content="55.86012186235461, -4.252010320043988">
    <meta name="geo.position" content="55.86012186235461;-4.252010320043988">
    <meta name="geo.region" content="GB-SCT">
    <meta name="geo.placename" content="Glasgow">
    <meta name="DC.title" content="{title}"/>

    <!-- Page Specific -->
    <meta name="rating" content="general">
    <meta name="subject" content="your document's subject">
    <meta name="description" content="A description of the page">

    <!-- site verification -->
{{#    <meta name="google-site-verification" content="verification_token"><!-- Google Search Console -->#}}
{{#    <meta name="yandex-verification" content="verification_token"><!-- Yandex Webmasters -->#}}
{{#    <meta name="msvalidate.01" content="verification_token"><!-- Bing Webmaster Center -->#}}
{{#    <meta name="alexaVerifyID" content="verification_token"><!-- Alexa Console -->#}}
{{#    <meta name="p:domain_verify" content="code_from_pinterest"><!-- Pinterest Console-->#}}
{{#    <meta name="norton-safeweb-site-verification" content="norton_code"><!-- Norton Safe Web -->#}}

    <!-- facebook -->
{{#    <meta property="fb:app_id" content="123456789">#}}
    <meta property="og:url" content="{{{{ request.base_url }}}}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Flask-Imp">
{{#    <meta property="og:image" content="~ static folder here ~/facebook-image.png">#}}
    <meta property="og:image:alt" content="A description of what is in the image (not a caption)">
    <meta property="og:description" content="Description Here">
    <meta property="og:site_name" content="Flask-Imp Website">
    <meta property="og:locale" content="en_GB">
    <meta property="article:author" content="">

    <!-- twitter -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:site" content="@site_account">
{{#    <meta name="twitter:creator" content="@individual_account">#}}
    <meta name="twitter:url" content="{{{{ request.base_url }}}}">
    <meta name="twitter:title" content="Flask-Imp Website">
    <meta name="twitter:description" content="Content description less than 200 characters">
{{#    <meta name="twitter:image" content="~ static folder here ~/twitter-image.png">#}}
    <meta name="twitter:image:alt" content="Description of the image (for visually impaired). Maximum 420 characters.">

    <!-- pinterest - disabled -->
    <meta name="pinterest" content="nopin">

    <!-- pre-loadings -->
{{#    https://css-tricks.com/prefetching-preloading-prebrowsing/ #}}
{{#    <link rel="dns-prefetch" href="//example.com/">#}}
{{#    <link rel="preconnect" href="https://www.example.com/">#}}
{{#    <link rel="prefetch" href="example.font.ttf">#}}
{{#    <link rel="prerender" href="https://example.com/">#}}
{{#    <link rel="preload" href="image.png" as="image">#}}

    <!-- favicons -->
{{#    <link rel="apple-touch-icon" sizes="152x152" href="~ static folder here ~/152x152-favicon.png">#}}
{{#    <link rel="icon" type="image/png" sizes="32x32" href="~ static folder here ~/32x32-favicon.png">#}}
{{#    <link rel="icon" type="image/png" sizes="16x16" href="~ static folder here ~/16x16-favicon.png">#}}
{{#    <link rel="manifest" href="~ static folder here ~/site.webmanifest">#}}

    <link rel="stylesheet" href="{{{{ url_for('{static_endpoint}', filename='css/water.css') }}}}">
    {js}

    <script>
        // inline script
    </script>
"""
