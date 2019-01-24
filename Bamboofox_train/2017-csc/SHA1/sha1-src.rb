#!/usr/bin/ruby

STDOUT.sync = true
require 'digest/sha1'
require 'base64'

flag = File.read("/home/ctf/flag")

puts "Can you login and get flag?"
puts "Enter username:"
username = Base64.decode64(gets.chomp)
puts "Enter password:"
password = Base64.decode64(gets.chomp)

if username != password and Digest::SHA1.hexdigest(username) == Digest::SHA1.hexdigest(password)
  puts flag
else
  puts "Wrong username and password!!!"
end
