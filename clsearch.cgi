#!/usr/bin/env perl
# $Id: clsearch.cgi,v 1.1 2002/06/29 03:37:25 yto Exp $
# clsearch.cgi - HTML �����줿 ChangeLog (by chalow) �򸡺�����CGI
use strict;

### User Setting from here
# �����ߤˤ��碌���Ѥ��Ʋ�����
my $home_page_url = "http://nais.to/~yto/";
my $home_page_name = "���Ĥ�Υۡ���ڡ���";
my $numnum = 20; # ���٤�ɽ���Ǥ����
my $css_file;
### to here

# nkf ��ư���� --- ���ܸ쥳���ɤ�Ǻ�ޤ���ʤ������...
my $NKF = `which nkf`;
chomp $NKF;
die "NO NKF!" if ($NKF !~ /nkf$/); 

use CGI;
my $q = new CGI;

my $myself = $q->url();		# ����CGI��URL
my $key = $q->param('key');
my $from = $q->param('from') || 0;

# ������ HTML head ���� ������
print $q->header();
print "<html><head><title>CHALOW Search</title>\n";
print "<meta http-equiv=\"Content-Type\"
                   content=\"text/html;charset=EUC-JP\">\n";
print qq(<link rel=stylesheet href="$css_file" media=all>\n)
    if defined $css_file;
print "</head><body>\n";

print qq(<a href="index.html">ChangeLog INDEX</a>
 / <a href="$home_page_url">$home_page_name</a>\n);
print $q->startform, $q->textfield('key'), $q->submit, $q->endform, "\n";

# ������ ���� ������
my $outstr = "";
my $cnt = 0;

if (defined $key) {
    my @fl = reverse sort <[0-9][0-9][0-9][0-9]-[0-9][0-9].html>;
    for my $fn (@fl) {
	open(F, "$NKF -e $fn |") or die "file open error: $fn\n";
	my $date = "";
	$/ = "";
	while (<F>) {
	    chomp;
	    s/<pre>\n//;	# for first day on the month
	    next unless (/^<a\sname/ or /^[\s\t]+\*/);
	    if (/^<.+?>(\d\d\d\d-\d\d-\d\d)</) {
		$date = $_;
		next;
	    } elsif (! /^[\s\t]+\*/) {
		next;
	    }

	    my $item = $_;

	    my $line = $date." ".$item;
	    $line =~ s/[\n\t]+//g; # ���Ծä�
	    $line =~ s/<.+?>//g; # ����ȴ��
	    
	    # $line �ǥѥ�����ޥå������ޥå������� $item ����Ϥ��롣
	    if ($line =~ m/$key/i) {
		$cnt++;

		my $ostr = "[$cnt] $date\n\n";

		# �������ʸ����ϥϥ��饤�Ȥ��ʤ�
		my @tmp = split(/(<.+?>)/, $item);
		foreach my $ii (@tmp) {
		    $ii =~ s|($key)|<font
			style="background-color: pink">$1</font>|gix
			    if ($ii !~ /^</);
		    $ostr .= $ii;
		}
		$ostr .= "\n\n";
		
		if ($cnt >= $from + 1 and
		    $cnt < $from + 1 + $numnum) {
		    $outstr .= $ostr;
		}
	    }
	}
	close F;
    }
}

my $page_max = int(($cnt - 1) / $numnum);

my ($qkey) = ($q->query_string =~ /(key=[^&]+)/);

# ������ ����ɽ���Τ���������� ������
my $bar = "";
if ($page_max != 0) { # 1�ڡ����ΤߤΤȤ����������ʤ�
    $bar = "<hr>\n";
    for (my $i = 0; $i <= $page_max; $i++) {
	if ($from / $numnum == $i) {
	    $bar .= $i + 1;
	} else {
	    $bar .= $q->a({-href => "$myself?from=".($i * $numnum)."&".$qkey},
			  $i + 1);
	}
	$bar .= " ";
    }
    $bar .= "(${numnum}�鷺��ɽ��)";
}

if ($cnt == 0) {
    print "���Ĥ���ޤ���Ǥ�����\n";
} else {
    print "$cnt �� ���Ĥ���ޤ�����\n";
}

print $bar;
print "<hr>\n";
print "\n<pre>",$outstr,"</pre>\n";
print $bar;
print "<hr>\n";

print qq(
<a href="index.html">ChangeLog INDEX</a>
 / <a href="$home_page_url">$home_page_name</a>
<div align="right">Powered by 
<a href="http://nais.to/~yto/tools/chalow/"><b>chalow</b></a></div>);

print $q->end_html(), "\n";

exit;
