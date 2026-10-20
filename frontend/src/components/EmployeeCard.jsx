import { CalendarDays, Mail } from "lucide-react";

export default function EmployeeCard({ employee }) {
  const joiningDate = new Date(
    `${employee.date_of_joining}T00:00:00`,
  ).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  return (
    <article className="employee-card">
      <div className="employee-avatar" aria-hidden="true">
        {employee.name
          .split(/\s+/)
          .filter(Boolean)
          .slice(0, 2)
          .map((part) => part[0])
          .join("")
          .toUpperCase()}
      </div>

      <div className="employee-details">
        <h3>{employee.name}</h3>
        <p className="employee-designation">{employee.designation}</p>

        <p className="employee-meta">
          <Mail size={15} aria-hidden="true" />
          <a href={`mailto:${employee.email}`}>{employee.email}</a>
        </p>

        <p className="employee-meta">
          <CalendarDays size={15} aria-hidden="true" />
          Joined {joiningDate}
        </p>
      </div>

      <span className="department-badge">{employee.department}</span>
    </article>
  );
}
