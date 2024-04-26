document.addEventListener('DOMContentLoaded', () => {
    // Manejar clics en enlaces de la barra lateral para cargar secciones
    const sidebarLinks = document.querySelectorAll('.sidebar a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) =>{
            e.preventDefault();
            const section = link.getAttribute('href').substring(1); // Obtiene el nombre de la sección desde href
            fetchSectionData(section);
        });
    });

});

function updateDOMWithHTML(html, section) {
    const sectionElement = document.getElementById(`${section}-section`);
    if (sectionElement) {
        sectionElement.innerHTML = html; // Asigna el HTML al innerHTML del elemento de la sección
        sectionElement.style.display = 'block'; // Muestra la sección
    }
    // Esconde las otras secciones
    const sections = document.querySelectorAll('.section');
    sections.forEach(sec => {
        if (sec.id !== `${section}-section`) {
            sec.style.display = 'none';
        }
    });
}
// Función para cambiar la sección visible basada en el identificador

function fetchSectionData(section) {
    const url = section === 'doctors' ? '/doctors' : `/${section}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Verifica el tipo de datos recibidos y actúa en consecuencia
            if (typeof data === 'string') {
                updateDOMWithHTML(data, section); // Si es HTML
            } else {
                // Asumiendo que existe una función para manejar datos JSON
                handleJSONData(data, section); // Si es JSON
            }
        })
        .catch(error => console.error('Error al cargar la sección:', error));
}

// Actualiza el DOM con el nuevo HTML
// Evento para manejar clics en la barra lateral
document.querySelectorAll('.sidebar a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Obtiene la sección del href del enlace
        const sectionId = this.getAttribute('href').split('#')[1];
        
        // Cambia la sección visible
        changeSection(sectionId);
        // Carga los datos para esa sección
        if (sectionId === 'doctors-section') {
          
            getDoctors();
        } else if (sectionId === 'patients-section') {
            getPatients();
        } else if (sectionId === 'appointments-section') {
            getAppointments();
        }
    });
});

function changeSection(sectionId) {
    console.log(`Cambiando a la sección: ${sectionId}`);
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });

    // Muestra la sección correspondiente
    const section = document.getElementById(sectionId);
    if (section) {
        section.style.display = 'block';
    }
}

function loadSpecialties() {
    fetch('/especialidad') // Asegúrate de que este endpoint exista y que tu servidor Flask esté corriendo
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(specialties => {
        const specialtySelect = document.getElementById('specialty-select');
        specialtySelect.innerHTML = '<option value=""></option>'; // Opción por defecto
        specialties.forEach(specialty => {
          const option = document.createElement('option');
          option.value = specialty.id;
          option.textContent = specialty.name;
          specialtySelect.appendChild(option);
        });
      })
      .catch(error => console.error('Error al cargar las especialidades:', error));
  }
  
  // Llama a loadSpecialties cuando sea adecuado, por ejemplo, al cargar la página o cuando el formulario de doctor se muestre:
  document.addEventListener('DOMContentLoaded', loadSpecialties);

function loadTypeCita() {
    fetch('/tipos_cita') // Asegúrate de que este endpoint exista y que tu servidor Flask esté corriendo
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(typecita => {
        const typeCitaSelect = document.getElementById('tipocita-select');
        typeCitaSelect.innerHTML = '<option value=""></option>'; // Opción por defecto
        typecita.forEach(typecita => {
          const option = document.createElement('option');
          option.value = specialty.id;
          option.textContent = specialty.name;
          specialtySelect.appendChild(option);
        });
      })
      .catch(error => console.error('Error al cargar los tipos de citas', error));
  }
  
  // Llama a loadSpecialties cuando sea adecuado, por ejemplo, al cargar la página o cuando el formulario de doctor se muestre:
  document.addEventListener('DOMContentLoaded', loadTypeCita);
  
// Funciones para manejar doctores
function getDoctors() {
    fetch('/doctors')
      .then(response => response.json())
      .then(doctors => {
        const doctorsList = document.getElementById('doctors-list');
        doctorsList.innerHTML = ''; // Limpiar lista existente
        doctors.forEach(doctor => {
          const listItem = document.createElement('li');
          listItem.innerHTML = `
            <p>Nombre: ${doctor.name}</p>
            <p>Especialidad: ${doctor.specialty.name}</p>
            <p>Cantidad de Citas: ${doctor.appointments_count}</p>
            <button onclick="deleteDoctor(${doctor.id})">Eliminar</button>
            <button onclick="editDoctor(${doctor.id})">Editar</button>
          `;
          doctorsList.appendChild(listItem);
        });
      })
      .catch(error => console.error('Error al obtener los doctores:', error));
}

function addDoctor() {
    const name = document.getElementById('doctor-name').value;
    const specialtySelect = document.getElementById('specialty-select');
    const specialtyId = specialtySelect.value;
  
    fetch('/doctors', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({name, specialty_id: specialtyId })
    })
    .then(response => response.json())
    .then(newDoctor => {
      getDoctors(); // Recargar lista de doctores
      document.getElementById('doctor-name').value = ''; // Limpiar campos del formulario
      specialtySelect.selectedIndex = 0; // Resetear el menú desplegable a la opción por defecto
    })
    .catch(error => console.error('Error al añadir un nuevo doctor:', error));
}
function deleteDoctor(id) {
    fetch(`/doctors/${id}`, {
      method: 'DELETE'
    })
    .then(response => {
      if (response.ok) {
        getDoctors(); // Recargar lista de doctores
      }
    });
}

function editDoctor(id) {
    // Obtiene los detalles del doctor por su id
    fetch(`/doctors/${id}`)
      .then(response => response.json())
      .then(doctor => {
        // Rellena el formulario con los datos actuales del doctor
        document.getElementById('edit-doctor-id').value = doctor.id;
        document.getElementById('edit-doctor-name').value = doctor.name;
        const specialtySelect = document.getElementById('edit-specialty-select');
        // Aquí debes asegurarte de que las especialidades estén cargadas en el select
        specialtySelect.value = doctor.specialty.id; // Asume que el select ya tiene las opciones de especialidades
        
        // Muestra el modal
        const modal = document.getElementById('edit-doctor-modal');
        modal.style.display = 'block';

        // Agrega el evento submit al formulario
        document.getElementById('edit-doctor-form').onsubmit = function(event) {
            event.preventDefault();
            submitEditDoctorForm();
        };

        // Cierra el modal al hacer clic en el botón de cierre
        document.querySelector('.close-button').onclick = function() {
            modal.style.display = 'none';
        };
      })
      .catch(error => console.error('Error al obtener los detalles del doctor:', error));
}

function submitEditDoctorForm() {
    const id = document.getElementById('edit-doctor-id').value;
    const name = document.getElementById('edit-doctor-name').value;
    const specialtyId = document.getElementById('edit-specialty-select').value;
    
    fetch(`/doctors/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, specialty_id: specialtyId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al actualizar el doctor');
        }
        return response.json();
    })
    .then(updatedDoctor => {
        // Actualizar la UI con los nuevos datos
        getDoctors();
        // Cerrar el modal
        document.getElementById('edit-doctor-modal').style.display = 'none';
    })
    .catch(error => {
        console.error('Error al actualizar el doctor:', error);
        alert('Hubo un error al actualizar la información del doctor.');
    });
}


function getPatients() {
    fetch('/patients')
      .then(response => response.json())
      .then(patients => {
        const patientsList = document.getElementById('patients-list');
        patientsList.innerHTML = '';
        patients.forEach(patient => {
          const listItem = document.createElement('li');
          listItem.innerHTML = 
          `<p>Nombre: ${patient.name}</p>
            <p>Edad: ${patient.age}</p>
          <button onclick="deleteDoctor(${patient.id})">Eliminar</button>
          <button onclick="editDoctor(${patient.id})">Editar</button>
          `
          patientsList.appendChild(listItem);
        });
      });
}

function addPatient() {
    const name = document.getElementById('patient-name').value;
    const age = document.getElementById('patient-age').value;

    const patientData = {
        name: name,
        age: age
    };

    fetch('/patients', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(patientData)
    })
    .then(response => response.json())
    .then(newPatient => {
        console.log('Paciente añadido:', newPatient);
        // Aquí podrías limpiar el formulario o actualizar la lista de pacientes
        document.getElementById('patient-name').value = '';
        document.getElementById('patient-age').value = '';
        // Opcional: Llamar a una función que recargue la lista de pacientes
    })
    .catch(error => console.error('Error al añadir un nuevo paciente:', error));
}


// Funciones para manejar citas
function getAppointments() {
    fetch('/citas')
      .then(response => response.json())
      .then(appointments => {
        const appointmentsList = document.getElementById('appointments-list');
        appointmentsList.innerHTML = '';
        appointments.forEach(appointment => {
          const listItem = document.createElement('li');
          listItem.innerHTML = `
          <p> Fecha: ${appointment.appointment_date}</p>
          <p> Tipo de Cita: ${appointment.tipo.nombre} </p>
          <p> Doctor: ${appointment.doctor.name} </p>
          <p> Paciente: ${appointment.patient.name}</p>
          <button onclick="deleteDoctor(${appointment.id})">Eliminar</button>
          <button onclick="editDoctor(${appointment.id})">Editar</button>
          `;
          appointmentsList.appendChild(listItem);
        });
      });
      
}


function loadOptions() {
    loadDoctors();
    loadPatients();
    loadTiposCita();
}

function loadDoctors() {
    fetch('/doctors')
        .then(response => response.json())
        .then(doctors => {
            const select = document.getElementById('doctor-select');
            doctors.forEach(doctor => {
                const option = new Option(doctor.name, doctor.id);
                select.add(option);
            });
        })
        .catch(error => console.error('Error al cargar doctores:', error));
}

function loadPatients() {
    fetch('/patients')
        .then(response => response.json())
        .then(patients => {
            const select = document.getElementById('patient-select');
            patients.forEach(patient => {
                const option = new Option(patient.name, patient.id);
                select.add(option);
            });
        })
        .catch(error => console.error('Error al cargar pacientes:', error));
}

function loadTiposCita() {
    fetch('/tipos_cita')
        .then(response => response.json())
        .then(tipos => {
            const select = document.getElementById('tipo-select');
            tipos.forEach(tipo => {
                const option = new Option(tipo.nombre, tipo.id);
                select.add(option);
            });
        })
        .catch(error => console.error('Error al cargar tipos de cita:', error));
}

document.addEventListener('DOMContentLoaded', loadOptions);

function addAppointment() {
    const doctorId = document.getElementById('doctor-select').value;
    const patientId = document.getElementById('patient-select').value;
    const tipoId = document.getElementById('tipo-select').value;
    const appointmentDate = document.getElementById('appointment-date').value;

    const appointmentData = {
        doctor_id: doctorId,
        patient_id: patientId,
        tipo_id: tipoId,
        appointment_date: appointmentDate
    };

    fetch('/citas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(appointmentData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Cita creada:', data);
        // Actualizar la interfaz del usuario para mostrar la nueva cita o un mensaje de confirmación
    })
    .catch(error => console.error('Error al crear la cita:', error));
}
