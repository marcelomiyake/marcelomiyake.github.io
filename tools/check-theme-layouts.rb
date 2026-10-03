# Fails when the installed Chirpy version differs from the version that the
# local layout overrides were copied from, so upgrades re-sync them on purpose.
# Usage: bundle exec ruby tools/check-theme-layouts.rb

OVERRIDES = {
  '_layouts/home.html' => '7.6.0'
}.freeze

installed = Gem.loaded_specs['jekyll-theme-chirpy']&.version&.to_s ||
            Gem::Specification.find_by_name('jekyll-theme-chirpy').version.to_s

stale = OVERRIDES.reject { |_, base| base == installed }
if stale.any?
  stale.each do |file, base|
    warn "#{file} is based on Chirpy #{base}, but #{installed} is installed. " \
         'Compare it with the new upstream layout, re-apply the local changes, and update this file.'
  end
  exit 1
end

puts "Theme layout overrides match Chirpy #{installed}."
