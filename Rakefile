require 'fileutils'
require 'rubygems'

require 'rake'

def python(input)
  sh "python #{input}"
end

def nosetests(input)
  sh "nosetests #{input}"
end

clean = namespace :clean do
  desc "Cleans the VIM leftouvers"
  task :vim do
    sh "find . -name '.*.sw[a-z]' -exec rm '{}' \\;"
  end

  desc "Cleans the Python bytecode leftouvers"
  task :py do
    sh "find . -name '*.py[co]' -exec rm '{}' \\;"
  end
end

desc "Cleans all"
task :clean => clean.tasks

desc "Runs pylint"
task :lint do
  sh "pylint -E app"
end

desc "Runs the tests"
task :test, :module do |t, args|
  args.with_defaults :module => :all

  case args[:module]
  when :all
    nosetests "-v -w tests"
  else
    nosetests "-v tests/test_#{args[:module]}.py"
  end
end

server = namespace :server do
  desc "Runs a development server"
  task :development do
    python "runner.py port=8080 debug=1"
  end

  desc "Runs a production server"
  task :production => [:dependent, :tasks] do
    python "runner.py port=80"
  end
end

git = namespace :git do
  desc "Adds all of the current files under git"
  task :add_files => [:clean] do
    sh "find . -exec git add '{}' \\;"
  end
end

task :default => [:clean, :lint, :test]

