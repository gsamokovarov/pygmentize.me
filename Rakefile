%w{rubygems rake}.each { |p| require p }

include(Module.new do
  include FileUtils

  %w{python nosetests pylint git}.each do |dep|
    define_method(dep) do |input = nil|
      sh "#{dep} #{Array === input ? ' '.join(input) : input}"
    end
  end

  self
end)

namespace :clean do
  desc "Cleans the VIM leftouvers"
  task :vim do
    Dir['**/.*.sw?'].each { |file| rm file }
  end

  desc "Cleans the Python bytecode leftouvers"
  task :py do
    Dir['**/*.pyc'].each { |file| rm file }
  end
end

desc "Cleans all"
task :clean => [:'clean:vim', :'clean:py']

desc "Runs pylint"
task(:lint) { pylint "-E app" }

desc "Runs the tests"
task(:test) { nosetests 'test' }

namespace :server do
  DEFAULT_DEVELOPMENT_PORT = 8000
  DEFAULT_PRODUCION_PORT = 80

  desc "Runs a development server"
  task :development do
    python "runner.py port=#{DEFAULT_DEVELOPMENT_PORT} debug=1 logging=debug"
  end

  desc "Runs a production server"
  task :production do
    python "runner.py port=#{DEFAULT_PRODUCION_PORT}"
  end
end

namespace :git do
  desc "Adds all of the current files under git"
  task :add_files => [:clean] do
    sh "find . | grep -v '.git' | xargs git add"
  end
end

task :default => [:clean, :lint, :test]
