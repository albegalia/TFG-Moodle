<?php
// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

use core_external\util as external_util;

/**
 * Teachers info block.
 *
 * @package   block_teachers_info
 * @license   http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

defined('MOODLE_INTERNAL') || die();

class block_teachers_info extends block_base {
    function init() {
        $this->title = get_string('pluginname', 'block_teachers_info');
    }

    function get_content() {

        if ($this->content !== NULL) {
            return $this->content;
        }

        $course = $this->page->course;
        $context = get_context_instance(CONTEXT_COURSE, $course->id);
        if (!has_capability('block/teachers_info:view', $context)) {
            return;
        }

        $url = 'https://tfgmoodleazureapp.azurewebsites.net/api/courselogins?code=codigo&id=' . $course->id;
        $html = file_get_contents($url);

        $this->content = new stdClass;
        $this->content->text = $html;

        return $this->content;
    }
}
