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

class local_send_events_observer
{
	//Cuando se hace login
	public static function user_loggedin(\core\event\user_loggedin $event)
    {
        $event_data = $event->get_data();
        $event_data['domain'] = 'tfgalberto@tfg.es';

        self::send_event_to_api($event_data);
    }

	//Cuando se sube una tarea
	public static function mod_assign_submission_created(\mod_assign\event\submission_created $event)
    {
        $event_data = $event->get_data();
        $event_data['domain'] = 'tfgalberto@tfg.es';

        self::send_event_to_api($event_data);
    }

    //Cuando se ve un documento
	public static function mod_resource_course_module_viewed(\mod_resource\event\course_module_viewed $event)
    {
        $event_data = $event->get_data();
        $event_data['domain'] = 'tfgalberto@tfg.es';
        
        self::send_event_to_api($event_data);
    }

    //Cuando se ha visitado un "external tool"
	public static function mod_lti_course_module_viewed(\mod_lti\event\course_module_viewed $event)
    {
        $event_data = $event->get_data();
        $event_data['domain'] = 'tfgalberto@tfg.es';
        
        self::send_event_to_api($event_data);
    }

    //Cuando se crea un modulo (crear tarea, subir documento, subir external tool, etc)
    public static function course_module_created(\core\event\course_module_created $event)
    {
        $event_data = $event->get_data();
        $event_data['domain'] = 'tfgalberto@tfg.es';
        
        self::send_event_to_api($event_data);
    }

    public static function send_event_to_api($data)
    {
        // Solicitud HTTP Post a Azure
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, "URL de la API donde enviamos los eventos");
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Authorization: Bearer Token'
        )); 

        $resultado = curl_exec($ch);

        // Verificar si hubo algun error en la formacion de la solicitud
        if (curl_errno($ch)) 
        {
            var_dump('Error en la solicitud');
            die();
        }
        // Obtener codigo de la respuesta HTTP
        $codigo_respuesta = curl_getinfo($ch, CURLINFO_HTTP_CODE);

        // Cerramos la sesion
        curl_close($ch);

        if ($codigo_respuesta == 201)
        {
            return true;
        }
        else 
        {
            var_dump("Codigo de respuesta: $codigo_respuesta");
            die();
        }
    }
}