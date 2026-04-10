/**
 * Modern Schedule Component
 * Responsive week/day view with mobile support
 */

class ModernSchedule {
  constructor(element) {
    this.element = element;
    this.timelineStart = 8 * 60; // 08:00 in minutes
    this.timelineEnd = 22 * 60;    // 22:00 in minutes
    this.hourHeight = 80;         // Height of one hour in pixels
    this.currentDayIndex = 0;     // For mobile day view
    this.days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'];
    
    this.init();
  }

  init() {
    this.setupMobileNavigation();
    this.positionAppointments();
    this.setupEventListeners();
    this.highlightCurrentTime();
    this.setupDaySelection();
    
    // Update current time line every minute
    setInterval(() => this.highlightCurrentTime(), 60000);
  }

  setupMobileNavigation() {
    // Add mobile day navigation if not exists
    if (!this.element.querySelector('.mobile-day-nav')) {
      const mobileNav = document.createElement('div');
      mobileNav.className = 'mobile-day-nav';
      mobileNav.innerHTML = `
        <button id="prev-day" aria-label="Dia anterior">
          <i class="bi bi-chevron-left"></i> Anterior
        </button>
        <span class="current-day-label">Segunda-feira</span>
        <button id="next-day" aria-label="Próximo dia">
          Próximo <i class="bi bi-chevron-right"></i>
        </button>
      `;
      
      const scheduleBody = this.element.querySelector('.schedule-body');
      if (scheduleBody) {
        scheduleBody.insertBefore(mobileNav, scheduleBody.firstChild);
      }
    }

    // Setup mobile nav buttons
    const prevBtn = this.element.querySelector('#prev-day');
    const nextBtn = this.element.querySelector('#next-day');
    
    if (prevBtn) {
      prevBtn.addEventListener('click', () => this.navigateDay(-1));
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.navigateDay(1));
    }

    // Show first day on mobile
    this.showDay(0);
  }

  navigateDay(direction) {
    const newIndex = this.currentDayIndex + direction;
    if (newIndex >= 0 && newIndex < this.days.length) {
      this.showDay(newIndex);
    }
  }

  showDay(index) {
    this.currentDayIndex = index;
    
    // Update day columns visibility
    const dayColumns = this.element.querySelectorAll('.day-column');
    dayColumns.forEach((col, i) => {
      if (i === index) {
        col.classList.add('active');
      } else {
        col.classList.remove('active');
      }
    });

    // Update mobile day label
    const dayLabels = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira'];
    const label = this.element.querySelector('.current-day-label');
    if (label) {
      label.textContent = dayLabels[index];
    }

    // Update header active state
    const headers = this.element.querySelectorAll('.schedule-day-header');
    headers.forEach((header, i) => {
      if (i === index) {
        header.classList.add('active');
      } else {
        header.classList.remove('active');
      }
    });

    // Update button states
    const prevBtn = this.element.querySelector('#prev-day');
    const nextBtn = this.element.querySelector('#next-day');
    
    if (prevBtn) {
      prevBtn.disabled = index === 0;
      prevBtn.style.opacity = index === 0 ? '0.5' : '1';
    }
    if (nextBtn) {
      nextBtn.disabled = index === this.days.length - 1;
      nextBtn.style.opacity = index === this.days.length - 1 ? '0.5' : '1';
    }
  }

  setupDaySelection() {
    // Click on day header to select that day (mobile)
    const headers = this.element.querySelectorAll('.schedule-day-header');
    headers.forEach((header, index) => {
      header.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
          this.showDay(index);
        }
      });
    });
  }

  positionAppointments() {
    const appointments = this.element.querySelectorAll('.appointment-card');
    
    appointments.forEach(appointment => {
      const startTime = appointment.dataset.start;
      const endTime = appointment.dataset.end;
      
      if (!startTime || !endTime) return;

      const start = this.timeToMinutes(startTime);
      const end = this.timeToMinutes(endTime);
      
      if (start === 0 && end === 0) return;

      const top = ((start - this.timelineStart) / 60) * this.hourHeight;
      const height = ((end - start) / 60) * this.hourHeight;

      appointment.style.top = `${top}px`;
      appointment.style.height = `${height}px`;

      // Determine period for styling
      const hour = Math.floor(start / 60);
      if (hour < 12) {
        appointment.classList.add('manha');
      } else if (hour < 18) {
        appointment.classList.add('tarde');
      } else {
        appointment.classList.add('noite');
      }
    });
  }

  timeToMinutes(time) {
    if (!time) return 0;
    
    time = time.replace(/\s/g, '');
    const parts = time.split(':');
    if (parts.length < 2) return 0;
    
    const hours = parseInt(parts[0], 10);
    const minutes = parseInt(parts[1], 10);
    
    if (isNaN(hours) || isNaN(minutes)) return 0;
    
    return hours * 60 + minutes;
  }

  highlightCurrentTime() {
    // Remove existing current time line
    const existing = this.element.querySelector('.current-time-line');
    if (existing) {
      existing.remove();
    }

    const now = new Date();
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    
    // Only show if within schedule hours
    if (currentMinutes < this.timelineStart || currentMinutes > this.timelineEnd) {
      return;
    }

    const top = ((currentMinutes - this.timelineStart) / 60) * this.hourHeight;
    
    const line = document.createElement('div');
    line.className = 'current-time-line';
    line.style.top = `${top}px`;
    
    // Add to each day column
    const dayColumns = this.element.querySelectorAll('.day-column');
    dayColumns.forEach(column => {
      const columnLine = line.cloneNode(true);
      column.appendChild(columnLine);
    });
  }

  setupEventListeners() {
    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        this.positionAppointments();
        this.handleResize();
      }, 250);
    });

    // Appointment click handlers
    const appointments = this.element.querySelectorAll('.appointment-card');
    appointments.forEach(apt => {
      apt.addEventListener('click', (e) => {
        e.preventDefault();
        this.openAppointmentModal(apt);
      });
    });
  }

  handleResize() {
    // Reset to appropriate view based on screen size
    if (window.innerWidth > 768) {
      // Desktop - show all days
      const dayColumns = this.element.querySelectorAll('.day-column');
      dayColumns.forEach(col => col.classList.add('active'));
    } else {
      // Mobile - show only current day
      this.showDay(this.currentDayIndex);
    }
  }

  openAppointmentModal(appointment) {
    const patientName = appointment.querySelector('.patient-name')?.textContent || 'Consulta';
    const doctorName = appointment.querySelector('.doctor-name')?.textContent || '';
    const timeRange = appointment.querySelector('.time-range')?.textContent || '';
    const startTime = appointment.dataset.start || '';
    const endTime = appointment.dataset.end || '';
    
    // Create modal if not exists
    let modal = document.querySelector('.schedule-modal-overlay');
    if (!modal) {
      modal = document.createElement('div');
      modal.className = 'schedule-modal-overlay';
      modal.innerHTML = `
        <div class="schedule-modal">
          <div class="schedule-modal-header">
            <button class="schedule-modal-close">
              <i class="bi bi-x-lg"></i>
            </button>
            <h3 class="modal-title">${patientName}</h3>
            <p class="modal-subtitle">${timeRange}</p>
          </div>
          <div class="schedule-modal-body">
            <div class="modal-info">
              <p><strong>Médico:</strong> ${doctorName}</p>
              <p><strong>Horário:</strong> ${startTime} - ${endTime}</p>
            </div>
            <div class="modal-actions">
              <button class="btn-modal btn-modal-primary" onclick="window.location.href='?edit=true'">
                <i class="bi bi-pencil"></i> Editar
              </button>
              <button class="btn-modal btn-modal-danger" onclick="if(confirm('Confirmar cancelamento?')) window.location.href='?cancel=true'">
                <i class="bi bi-x-circle"></i> Cancelar
              </button>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(modal);

      // Close handlers
      modal.querySelector('.schedule-modal-close').addEventListener('click', () => {
        modal.classList.remove('active');
      });
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          modal.classList.remove('active');
        }
      });
    } else {
      // Update existing modal content
      modal.querySelector('.modal-title').textContent = patientName;
      modal.querySelector('.modal-subtitle').textContent = timeRange;
      const infoDiv = modal.querySelector('.modal-info');
      infoDiv.innerHTML = `
        <p><strong>Médico:</strong> ${doctorName}</p>
        <p><strong>Horário:</strong> ${startTime} - ${endTime}</p>
      `;
    }

    // Show modal
    requestAnimationFrame(() => {
      modal.classList.add('active');
    });
  }

  // Public method to refresh appointments
  refresh() {
    this.positionAppointments();
    this.highlightCurrentTime();
  }

  // Public method to go to specific day
  goToDay(dayIndex) {
    if (dayIndex >= 0 && dayIndex < this.days.length) {
      this.showDay(dayIndex);
    }
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  const scheduleElements = document.querySelectorAll('.modern-schedule');
  
  window.modernSchedules = [];
  scheduleElements.forEach((element, index) => {
    window.modernSchedules.push(new ModernSchedule(element));
  });
});

// Expose to global scope for manual initialization
window.ModernSchedule = ModernSchedule;
