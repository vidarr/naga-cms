#
# Part of the CMS naga, See <https://ubeer.org>
#
#    Copyright (C) 2015 Michael J. Beer <michael.josef.beer@googlemail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
def wsgi_start_response(start_response_callback, status = '200 OK'):
    '''
    Create appropriate HTTP header
    '''
    response_headers = [('Content-Type', 'text/html')]
    start_response_callback(status, response_headers)
    
