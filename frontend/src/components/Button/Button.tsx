import './Button.css'
type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  text: string;
  secondary?: boolean;
};

function Button({
  text,
  secondary,
  ...props
}: ButtonProps) {
  return (
    <button
      {...props}
     className={`btn ${secondary ? 'btn-secondary' : 'btn-primary'}`}
    >
      {text}
    </button>
  );
}

export default Button;