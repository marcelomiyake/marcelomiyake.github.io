# Inline render-blocking CSS and the tiny theme-mode initializer. The compressed
# styles are small; embedding them avoids serial requests before the first paint.
# Deferred scripts and fonts retain their browser cache benefits.
require 'nokogiri'

Jekyll::Hooks.register :site, :post_render do |site|
  read_asset = lambda do |url|
    path = url.delete_prefix(site.baseurl.to_s).delete_prefix('/')
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
