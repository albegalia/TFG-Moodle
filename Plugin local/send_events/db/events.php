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

defined('MOODLE_INTERNAL') || die();

$observers = array(
    //Cuando se hace login
    array(
        'eventname' => '\core\event\user_loggedin',
        'callback' => 'local_send_events_observer::user_loggedin',
    ),
    //Cuando se sube una tarea
    array(
        'eventname' => '\mod_assign\event\submission_created',
        'callback' => 'local_send_events_observer::mod_assign_submission_created',
    ),
    //Cuando se ve un documento
    array(
        'eventname' => '\mod_resource\event\course_module_viewed',
        'callback' => 'local_send_events_observer::mod_resource_course_module_viewed',
    ),
    //Cuando se ha visitado un "external tool"
    array(
        'eventname' => '\mod_lti\event\course_module_viewed',
        'callback' => 'local_send_events_observer::mod_lti_course_module_viewed',
    ),
    //Cuando se crea un modulo (crear tarea, subir documento, subir external tool, etc)
    array(
        'eventname' => '\core\event\course_module_created',
        'callback' => 'local_send_events_observer::course_module_created',
    ),
);