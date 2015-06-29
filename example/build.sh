#!/bin/sh
thrift -r --gen py:new_style -out ./py definition/tutorial.thrift
thrift -r --gen php -out ./php definition/tutorial.thrift
