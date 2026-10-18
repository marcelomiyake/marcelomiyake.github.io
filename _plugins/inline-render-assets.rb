# Inline render-blocking CSS and the tiny theme-mode initializer. The compressed
# styles are small; embedding them avoids serial requests before the first paint.
# Deferred scripts and fonts retain their browser cache benefits.
require 'nokogiri'

Jekyll::Hooks.register :site, :post_render do |site|
  # Polyglot excludes `assets` from non-default languages, so their pages would
  # otherwise get the theme's stylesheet instead of the site's Sass override.
  overrides = {}
  render_override = lambda do |path|
    next overrides[path] if overrides.key?(path)

    dir = File.dirname(path)
    name = "#{File.basename(path, '.css')}.scss"
    next overrides[path] = nil unless path.end_with?('.css') && File.file?(File.join(site.source, dir, name))

    page = Jekyll::Page.new(site, site.source, dir, name)
    # The theme's stylesheet shares this path in Liquid's template cache.
    site.liquid_renderer.cache.delete(page.relative_path)
    overrides[path] = Jekyll::Renderer.new(site, page, site.site_payload).run
  end

  read_asset = lambda do |url|
    path = url.delete_prefix(site.baseurl.to_s).delete_prefix('/')
    override = render_override.call(path)
    next override if override
    rendered = site.pages.find { |asset| asset.url.delete_prefix('/') == path }
    next rendered.output if rendered
    [site.source, site.theme.root].each do |root|
      file = File.join(root, path)
      break File.read(file) if File.file?(file)
    end
  end

  (site.pages + site.collections.values.flat_map(&:docs)).each do |page|
    next unless page.output_ext == '.html'

    html = Nokogiri::HTML(page.output)
    html.css('link[rel="stylesheet"]').each do |link|
      next unless link['href'].start_with?('/')
      css = read_asset.call(link['href'])
      next unless css.is_a?(String)
      # Relative font URLs need their original stylesheet's base directory.
      directory = File.dirname(link['href'])
      css = css.gsub(/url\(["']?([^\)"']+)["']?\)/) do |match|
        url = Regexp.last_match(1)
        url.start_with?('/', 'data:', 'https:') ? match : "url(\"#{directory}/#{url}\")"
      end
      style = Nokogiri::XML::Node.new('style', html)
      style.content = css
      link.replace(style)
    end
    script = html.at_css('script[src$="/assets/js/dist/theme.min.js"]')
    if script
      script.content = read_asset.call(script['src'])
      script.remove_attribute('src')
    end
    page.output = html.to_html
  end
end
