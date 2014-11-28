FROM kb/base


# This seems to enable running the "source" command for rvm
#RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN sudo apt-get -y update
RUN sudo apt-get -y upgrade
# RUN source /usr/local/rvm/scripts/rvm

# Install Ruby and Bundler
RUN sudo apt-get -y install ruby
RUN gem install bundler

# installing system wide dependencies via tmp allows docker to cache the commands
WORKDIR /tmp
# install ruby gems from Gemfile
ADD Gemfile /tmp/Gemfile
ADD Gemfile.lock /tmp/Gemfile.lock
RUN bundle install

# add Flask and requirements
ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r requirements.txt


ADD . /home/app/
WORKDIR /home/app

# might want to run bower as non-root
RUN bower install --allow-root




# Enable uWSGI and nginx
# RUN rm -f /etc/service/uwsgi/down /etc/service/nginx/down
# RUN mkdir -p instance/
# RUN cp -n settings.staging.cfg instance/settings.cfg

CMD python /home/app/wsgi.py
