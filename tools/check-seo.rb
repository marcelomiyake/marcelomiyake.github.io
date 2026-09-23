# Run after a production build: bundle exec ruby tools/check-seo.rb
require 'nokogiri'
require 'json'
require 'uri'

files = Dir['_site/**/*.html']
abort 'Build _site first.' if files.empty?
descriptions = {}
files.each do |file|
  html = Nokogiri::HTML(File.read(file))
  %w[title h1].each do |selector|
    abort "#{file}: expected one #{selector}" unless html.css(selector).size == 1
  end
  ['meta[name="description"]', 'meta[name="robots"]',
   'link[rel="canonical"]', 'meta[property="og:image"]',
   'meta[property="twitter:image"]'].each do |selector|
    abort "#{file}: expected one #{selector}" unless html.css(selector).size == 1
  end
  canonical = URI(html.at_css('link[rel="canonical"]')['href'])
  abort "#{file}: invalid canonical" unless canonical.scheme == 'https' && canonical.host
  abort "#{file}: image missing alt" unless html.css('img:not([alt])').empty?
  html.css('script[type="application/ld+json"]').each { |node| JSON.parse(node.text) }
  robots = html.at_css('meta[name="robots"]')['content']
  if file == '_site/404.html'
    abort '404 must be noindex' unless robots.include?('noindex')
    next
  end
  abort "#{file}: unexpectedly noindex" if robots.include?('noindex')
  description = html.at_css('meta[name="description"]')['content']
  abort "#{file}: empty description" if description.to_s.strip.empty?
  abort "#{file}: description duplicates #{descriptions[description]}" if descriptions[description]
  descriptions[description] = file
end
%w[robots.txt sitemap.xml].each do |file|
  abort "Missing #{file}" unless File.file?("_site/#{file}")
end
puts "SEO checks passed for #{files.size} pages."
