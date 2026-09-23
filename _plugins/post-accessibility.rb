# Fix theme markup at build time, including pages without JavaScript.
require 'nokogiri'

Jekyll::Hooks.register [:pages, :documents], :post_render do |page|
  next unless page.output_ext == '.html'

  portuguese = page.data['lang'] == 'pt-BR'
  html = Nokogiri::HTML(page.output)
  if page.site.active_lang == 'pt-BR' && (portuguese || page.data['layout'] == 'home')
    html.at_css('html')['lang'] = 'pt-BR'
  end
  html.css('a.anchor').each do |anchor|
    label = portuguese ? 'Link para' : 'Link to'
    anchor['aria-label'] = "#{label} #{anchor.parent.text.strip}"
  end
  html.css('.post-navigation a[aria-label]').each do |link|
    if portuguese
      link['aria-label'] = "#{link['aria-label'] == 'Older' ? 'Postagem anterior' : 'Postagem mais recente'}: #{link.text.strip}"
    else
      link['aria-label'] = "#{link['aria-label']}: #{link.text.strip}"
    end
  end
  html.css('.toc-trigger').each { |button| button['aria-label'] = portuguese ? 'Conteúdo' : 'Contents' }
  html.at_css('#back-to-top')&.[]=('aria-label', portuguese ? 'Voltar ao topo' : 'Back to top')
  html.at_css('meta[name="viewport"]')&.[]=('content', 'width=device-width, initial-scale=1, viewport-fit=cover')
  page.output = html.to_html
end
