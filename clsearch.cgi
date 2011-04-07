#!/usr/bin/env perl
# $Id: clsearch.cgi,v 1.8 2003/06/22 03:04:09 yto Exp $
# clsearch.cgi - HTML �����줿 ChangeLog (by chalow) �򸡺�����CGI
use strict;

### User Setting from here
# �����ߤˤ��碌���Ѥ��Ʋ�����
my $home_page_url = "http://nais.to/~yto/";
my $home_page_name = "���Ĥ�Υۡ���ڡ���";
my $numnum = 20; # ���٤�ɽ���Ǥ����
my $css_file = "diary.css";
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
print "Content-type: text/html; charset=euc-jp\n\n";
print qq(<html><head><title>CHALOW Search</title>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">);
print qq(<link rel=stylesheet href="$css_file" media=all>\n)
    if defined $css_file;
print qq(</head><body><a href="index.html">ChangeLog INDEX</a>
 / <a href="$home_page_url">$home_page_name</a>\n);
print $q->startform, $q->textfield('key'), $q->submit, $q->endform, "\n";

# ������ ���� ������
my $outstr = "";
my $cnt = 0;

if (defined $key) {
    my @fl = reverse sort <[0-9][0-9][0-9][0-9]-[0-9][0-9].html>;
    for my $fn (@fl) {
	open(F, "$NKF -ed $fn |") or die "file open error: $fn\n";
	my $all = join('', <F>);
	close(F);

	my $date = "";
	while ($all =~ m!(<div\sclass=("day">.+?</h2>
				       |"section">.+?</div>))!gsmx) {
	    my $item = $1;
	    if ($2 =~ /^"day"/) {
		$date = $item;
		next;
	    }

	    my $tmpi = $item;
	    $tmpi =~ s/[\n\t]+//g; # ���Ծä�
	    $tmpi =~ s/<.+?>//g; # ����ȴ��

	    if ($tmpi =~ m/$key/i) {
		$cnt++;
		next if ($cnt < $from + 1 or $cnt >= $from + 1 + $numnum);
		my $ostr = "[$cnt] $date\n";
		# �������ʸ����ϥϥ��饤�Ȥ��ʤ�
		my @tmp = split(/(<.+?>)/, $item);
		foreach my $ii (@tmp) {
		    $ii =~ s|($key)|<strong 
			style="background-color:yellow">$1</strong>|gix
			    if ($ii !~ /^</);
		    $ostr .= $ii;
		}
		$outstr .= $ostr."</div>\n";
	    }
	}
    }
}

my $page_max = int(($cnt - 1) / $numnum);

my ($qkey) = ($q->query_string =~ /(key=[^&]+)/);

# ������ ����ɽ���Τ���������� ������
my $bar = "";
my ($navip, $navin);
if ($page_max != 0) { # 1�ڡ����ΤߤΤȤ����������ʤ�
    for (my $i = 0; $i <= $page_max; $i++) {
	if ($from / $numnum == $i) {
	    $bar .= "<strong>".($i + 1).'</strong>';
	} else {
	    $bar .= $q->a({-href => "$myself?from=".($i * $numnum)."&".$qkey},
			  $i + 1);
	}
	$bar .= " ";

	if ($from / $numnum == $i - 1) {
	    $navin = $q->a({-href => "$myself?from=".($i * $numnum).
				"&".$qkey}, "[ ���� ]");
	} elsif ($from / $numnum == $i + 1) {
	    $navip = $q->a({-href => "$myself?from=".($i * $numnum).
				"&".$qkey}, "[ ���� ]");
	}

    }
#    $bar .= "(${numnum}�鷺��ɽ��)";
}

if ($cnt == 0) {
    print "<p>���Ĥ���ޤ���Ǥ�����</p>\n";
} else {
    print "<p>$cnt �� ���Ĥ���ޤ�����</p>\n";
}

print qq(<p>$navip $bar $navin</p><pre>$outstr</pre><p>$navip $bar $navin</p>
<a href="index.html">ChangeLog INDEX</a>
 / <a href="$home_page_url">$home_page_name</a>
<div style="text-align:right">Powered by 
<a href="http://nais.to/~yto/tools/chalow/"><strong>chalow</strong></a></div>);

print $q->end_html(), "\n";

exit;
