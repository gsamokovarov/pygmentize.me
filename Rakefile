require 'fileutils'
require 'rubygems'

require 'rake'

def nosetests(input)
  sh "nosetests #{input}"
end

clean = namespace :clean do
  desc "Cleans the VIM leftouvers"
  task :vim do
    Dir['.*.sw[a-z]', '*/.*.sw[a-z]'].each { |fn|
      FileUtils.rm fn
    }
  end

  desc "Cleans the Python bytecode leftouvers"
  task :py do
    Dir['*.py[co]', '*/*.py[co]'].each { |fn|
      FileUtils.rm fn
    }
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

task :default => [:clean, :lint, :test]

