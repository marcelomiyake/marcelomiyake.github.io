# frozen_string_literal: true

# jekyll-sitemap adds these generated pages after Polyglot's localization
# exclusions have been applied. Keep the site's sitemap and robots file at
# the root instead of writing default-language copies under /pt-BR/.
Jekyll::Hooks.register :site, :post_render do |site|
  next if site.active_lang == site.default_lang

  site.pages.reject! { |page| %w[sitemap.xml robots.txt].include?(page.name) }
end
