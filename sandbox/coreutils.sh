#!/bin/bash

# brew install coreutils                                                                                                                                                                                   for cmd in cat date echo readlink sed basename;
do
  mkdir -p ~/.bin
  (test -e ~/.bin/$cmd) || (ln -s $(which g$cmd) ~/.bin/$cmd)
done
export PATH=~/.bin:$PATH
